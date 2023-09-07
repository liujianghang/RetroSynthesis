package com.whu.retrosynthesis.service.serviceImpl;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.bean.copier.CopyOptions;
import cn.hutool.core.lang.UUID;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.whu.retrosynthesis.mapper.UserMapper;
import com.whu.retrosynthesis.pojo.User;
import com.whu.retrosynthesis.pojo.UserDTO;
import com.whu.retrosynthesis.service.UserService;
import com.whu.retrosynthesis.utils.MD5Utils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import static com.whu.retrosynthesis.utils.RedisConstants.LOGIN_USER_KEY;
import static com.whu.retrosynthesis.utils.RedisConstants.LOGIN_USER_TTL;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    /**
     * 简单实现用户的注册功能
     *
     * @param user
     * @return
     */
    @Override
    public int registerUser(User user) {
        // 在这里执行用户注册逻辑，将用户信息插入数据库
        // 检查该用户是否存在
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("username", user.username);
        int userCheck = userMapper.selectCount(queryWrapper);
        if (userCheck > 0) {
            return 0;
        }
        // 加密存储
        user.setPassword(MD5Utils.inputPassToFormPass(user.getPassword()));
        return userMapper.insert(user);
    }

    /**
     * 实现用户的登录功能
     *
     * @param username
     * @param password
     * @return
     */
    @Override
    public int loginUser(String username, String password, HttpServletRequest request, HttpServletResponse response) {
        // 在这里执行用户登录逻辑，查询数据库验证用户名密码
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("username", username);
        User user = userMapper.selectOne(queryWrapper);
        if (user == null) {
            return 0;
        }
        if (!MD5Utils.inputPassToFormPass(password).equals(user.getPassword())) {
            return 2;
        }
        // 查看是否有token
        String requestToken = request.getHeader("token");
        String requestTokenKey = LOGIN_USER_KEY + requestToken;
        // 检查是否已存在对应的 Redis key
        Boolean exists = stringRedisTemplate.hasKey(requestTokenKey);
        if (Boolean.TRUE.equals(exists)) {
            response.addHeader("token", requestToken);
            return 1;
        }
        // 否则产生新的id
        String token = UUID.randomUUID().toString(true);
        String tokenKey = LOGIN_USER_KEY + token;

        // 转换
        UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);
        Map<String, Object> userMap = BeanUtil.beanToMap(userDTO, new HashMap<>(),
                CopyOptions.create()
                        .setIgnoreNullValue(true)
                        .setFieldValueEditor((fieldName, fieldValue) -> fieldValue.toString()));
        if (Boolean.FALSE.equals(exists)) {
            stringRedisTemplate.opsForHash().putAll(tokenKey, userMap);
            stringRedisTemplate.expire(tokenKey, LOGIN_USER_TTL, TimeUnit.MINUTES); // 设置有效期
            // response
            response.addHeader("token", token);
        }
        return 1;
    }
}
