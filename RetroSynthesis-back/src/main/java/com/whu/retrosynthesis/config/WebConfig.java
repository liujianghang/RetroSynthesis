package com.whu.retrosynthesis.config;

import com.whu.retrosynthesis.utils.LoginInterceptor;
import com.whu.retrosynthesis.utils.RefreshTokenInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import javax.annotation.Resource;

/**
 * 解决跨域问题
 * 1.在项目中创建一个新的配置文件
 * 2.添加@Configuration注解实现WebMvcConfigurer接口
 * 3.重写addCorsMappings方法并设置允许跨域的代码
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Resource
    private LoginInterceptor loginInterceptor;
    @Resource
    private RefreshTokenInterceptor refreshTokenInterceptor;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // 所有接口
                .allowCredentials(true) // 是否发送 Cookie
                .allowedOriginPatterns("*") // 支持域
                .allowedMethods("GET", "POST", "PUT", "DELETE") // 支持方法
                .allowedHeaders("*")
                .exposedHeaders("*");
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // token刷新拦截器
        registry.addInterceptor(refreshTokenInterceptor)
                .addPathPatterns("/**").order(1); // 顺序优先级，越高越先执行
        // 登录拦截器
        registry.addInterceptor(loginInterceptor)
                // ** 排除不需要登录拦截器拦截的路径
                .excludePathPatterns(
                        "/api/user/login",
                        "/api/user/register"
                ).order(2);
    }
}
