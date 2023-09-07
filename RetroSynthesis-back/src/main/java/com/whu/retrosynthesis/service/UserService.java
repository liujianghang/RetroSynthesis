package com.whu.retrosynthesis.service;


import com.baomidou.mybatisplus.extension.service.IService;
import com.whu.retrosynthesis.pojo.User;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public interface UserService extends IService<User> {
    int registerUser(User user);
    int loginUser(String username, String password, HttpServletRequest request, HttpServletResponse response);
}
