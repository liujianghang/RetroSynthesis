package com.whu.retrosynthesis.controller;

import com.whu.retrosynthesis.pojo.User;
import com.whu.retrosynthesis.service.UserService;
import com.whu.retrosynthesis.utils.Result;
import com.whu.retrosynthesis.utils.ResultEnum;
import com.whu.retrosynthesis.utils.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    private UserService userService;


    /**
     * 查询用户信息
     *
     * @param userId
     * @return user
     */
    @RequestMapping("/getUserInfo")
    public User getUserInfo(String userId) {
        User user = userService.getById(userId);
        return user;
    }

    /**
     * 测试：新增一个用户信息
     */
    @RequestMapping("/saveUser")
    public void saveUser() {
        User user = new User();
        user.setUsername("测试人员");
        user.setAccount("123456789");
        user.setPassword("123456");
        userService.save(user);
    }

    /**
     * 测试：post:新增一个用户信息
     */
    @RequestMapping(value = "/saveUser1", method = RequestMethod.POST)
    public int saveUser1(@RequestBody User user) {
        userService.save(user);
        return 1;
    }

    /**
     * 测试：根据id修改用户信息
     */
    @RequestMapping("/updateUser")
    public void updateUser() {
        User user = new User();
        user.setUid(999L);
        userService.updateById(user);
    }

    /**
     * 测试：删除一个用户
     *
     * @param userId
     */
    @RequestMapping("/deleteUser")
    public void deleteInfo(String userId) {
        userService.removeById(userId);
    }
    /**************
     *
     */
    /**
     * 测试：注册
     *
     * @param user
     * @return
     */
    @RequestMapping(value = "/register", method = RequestMethod.POST)
    public Result registerUser(@RequestBody User user) {
        int result = userService.registerUser(user);
        // 用户存在
        if (result == 0) {
            return ResultUtil.defineFail(ResultEnum.FAIL.code, "用户已经存在");
        }
        return ResultUtil.defineSuccess(ResultEnum.SUCCESS.code, "注册成功");
    }

    @RequestMapping(value = "/login", method = RequestMethod.POST)
    public Result loginUser(@RequestParam String username, @RequestParam String password, HttpServletRequest request, HttpServletResponse response) {

        int result = userService.loginUser(username, password, request,response);
        if (result == 0) {
            return ResultUtil.defineFail(ResultEnum.FAIL.code, "用户不存在");
        } else if (result == 2) {
            return ResultUtil.defineFail(ResultEnum.FAIL.code, "密码错误");
        }
        // 随机生成一个token
        return ResultUtil.defineSuccess(ResultEnum.SUCCESS.code, "登陆成功");
    }
}
