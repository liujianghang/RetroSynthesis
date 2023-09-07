package com.whu.retrosynthesis.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

// 说明该实体类对应于数据库的user表
@Data
@TableName("user")//@TableName中的值对应着表名
public class User {
    // 注意属性名要与数据表中的字段名一致

    @TableId(type = IdType.AUTO)
    public Long uid;
    // username
    public String username;
    // account
    public String account;
    // phone
    public String phone;
    // email
    public String email;
    // avatar
    public String avatar;
    // password
    private String password;

}
