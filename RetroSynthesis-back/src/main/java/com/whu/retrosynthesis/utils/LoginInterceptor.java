package com.whu.retrosynthesis.utils;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 登录拦截器
 */
@Component
public class LoginInterceptor  implements HandlerInterceptor {
    /**
     * 进入controller之前做登录校验
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 1. 判断是否需要拦截(ThreadLocal中是否有用户)
        // 跨域问题，放行OPTIONS请求
        String method = request.getMethod();
        if ("OPTIONS".equals(method)) {
            return true;
        }
        if (UserHolder.getUser() == null) {
            String jsonString = JSONObject.toJSONString(ResultUtil.defineFail(401, "用户未登录"));
            response.getWriter().write(jsonString);
            return false;
        }
        // 由用户，则放行
        return true;
    }
}
