package com.whu.retrosynthesis.pojo;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import java.time.LocalDateTime;


// 说明该实体类对应于数据库的molecule表
@Data
@TableName("molecule")//@TableName中的值对应着表名
public class Molecule {
    @TableId(type = IdType.AUTO) // 主键和自增策略
    public Long id;
    // smiles
    private String smiles;
    // cid
    private Integer cid;
    // bestRoute
    @TableField("bestPath")
    private String bestPath;
    // bestLength
    @TableField("bestLength")
    private Integer bestLength;
    // createTime
    @TableField(value = "createTime", fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}
