package com.whu.retrosynthesis.utils;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.util.StrUtil;
import com.whu.retrosynthesis.pojo.UserDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import static com.whu.retrosynthesis.utils.RedisConstants.LOGIN_USER_KEY;
import static com.whu.retrosynthesis.utils.RedisConstants.LOGIN_USER_TTL;

/**
 * 拦截一切路径
 * 1. 保存用户到Threadlocal
 * 2. 刷新token有效期
 */
@Component
public class RefreshTokenInterceptor implements HandlerInterceptor {
    @Autowired
    StringRedisTemplate stringRedisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        String token = request.getHeader("token");
        // 判空语句 不需要登陆的页面访问时 也得刷新token有效期
        if (StrUtil.isBlank(token)) {
            return true;
        }
        String tokenKey = LOGIN_USER_KEY + token;
        Map<Object, Object> userMap = stringRedisTemplate.opsForHash().entries(tokenKey); // .entries(tokenKey) 返回map
        if (userMap.isEmpty()) {
            // 4. 不存在，拦截, 返回401状态码
            // response.setStatus(401);
            return true;
        }
        // 存在转为 UserDTO
        UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);
        UserHolder.saveUser(userDTO);
        stringRedisTemplate.expire(tokenKey, LOGIN_USER_TTL, TimeUnit.MINUTES);
        // 放行
        return true;
    }
}
