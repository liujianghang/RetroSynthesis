package com.whu.retrosynthesis.pojo;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("user_molecule")
public class UserMolecule {

    @TableId(type = IdType.AUTO)
    private Long id;

    @TableField("userId")
    private Long userId;

    @TableField("moleculeId")
    private Long moleculeId;

    @TableField("expansionTopk")
    private Integer expansionTopk;

    @TableField("iteration")
    private Integer iteration;

    @TableField("processingTime")
    private Float processingTime;

    @TableField(value = "createTime", fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField("isSuccess")
    private Boolean isSuccess;

}
