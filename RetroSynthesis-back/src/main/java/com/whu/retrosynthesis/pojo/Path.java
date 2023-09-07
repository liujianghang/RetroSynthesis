package com.whu.retrosynthesis.pojo;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("path")//@TableName中的值对应着表名
public class Path {

    @TableId(type = IdType.AUTO)
    private Long id;
    // path
    private String path;
    // createDate
    @TableField(value = "createTime", fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    // molecule_id
    @TableField("moleculeId")
    private Long moleculeId;

}
