package com.whu.retrosynthesis.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.whu.retrosynthesis.pojo.Path;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Repository
@Mapper
public interface PathMapper extends BaseMapper<Path> {
}
