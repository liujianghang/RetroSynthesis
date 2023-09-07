package com.whu.retrosynthesis.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/redis")
public class RedisController {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @GetMapping(value = "/getUserByRedis")
    public String getIndex(){
        stringRedisTemplate.opsForValue().set("xiaocai", "888");
        String res = stringRedisTemplate.opsForValue().get("xiaocai");
        System.out.println(res);
        return res;
    }
}