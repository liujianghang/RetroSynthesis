package com.whu.retrosynthesis.utils;

import com.whu.retrosynthesis.pojo.UserDTO;

/**
 * 使用ThreadLocal存储用户信息
 * UserHolder是一个启用ThreadLocal的类
 */
public class UserHolder {
    /**
     * 每个使用该变量的线程都会初始化一个完全独立的实例副本。ThreadLocal 变量通常被private static修饰。
     * 当一个线程结束时，它所使用的所有 ThreadLocal 相对的实例副本都可被回收
     */
    private static final ThreadLocal<UserDTO> tl = new ThreadLocal<>();

    public static void saveUser(UserDTO user){
        tl.set(user);
    }

    public static UserDTO getUser(){
        return tl.get();
    }

    public static void removeUser(){
        tl.remove();
    }
}
