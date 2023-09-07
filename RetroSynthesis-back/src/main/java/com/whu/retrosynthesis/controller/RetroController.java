package com.whu.retrosynthesis.controller;

import cn.hutool.json.JSONObject;
import com.whu.retrosynthesis.pojo.Retro;
import com.whu.retrosynthesis.service.RetroService;
import com.whu.retrosynthesis.utils.Result;
import com.whu.retrosynthesis.utils.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/retro")
public class RetroController {

    @Autowired
    private RetroService retroService;

//    @RequestMapping(value = "/plan",method = RequestMethod.POST)
//    public Result getRetro(@RequestBody Retro retro) {
//        String url = "http://localhost:5001/api/retro/plan"; // 替换为实际的URL
//        JSONObject json;
//        try {
//           json = restTemplate.postForEntity(url, retro, JSONObject.class).getBody();
//        }catch (Exception e){
//            return ResultUtil.defineFail(500,"服务器错误");
//        }
//        return ResultUtil.success(json);
//    }
    @RequestMapping(value = "/plan",method = RequestMethod.POST)
    public Result getRetro(@RequestBody Retro retro) {
        JSONObject jsonResult;
        try {
            jsonResult = retroService.planRoutes(retro);
        } catch (Exception e) {
            return ResultUtil.defineFail(500, "服务器错误");
        }
        System.out.println("success!!!!!!");
        return ResultUtil.success(jsonResult);
    }
}
