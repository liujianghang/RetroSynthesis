package com.whu.retrosynthesis.service;

import cn.hutool.json.JSONObject;
import com.whu.retrosynthesis.pojo.Retro;

public interface RetroService {
    JSONObject planRoutes(Retro retro);
}
