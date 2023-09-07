package com.whu.retrosynthesis.pojo;

import lombok.Data;

/**
 * 隐藏用户敏感信息
 */
@Data
public class UserDTO {
    public Long uid;
    // username
    public String username;
}
