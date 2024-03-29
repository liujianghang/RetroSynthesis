package com.whu.retrosynthesis.utils;


public class ResultUtil {

    public static <T> Result<T> defineSuccess(Integer code, T data) {
        Result<Object> result = new Result<>();
        return result.setCode(code).setData(data);
    }

    public static <T> Result<T> success(T data) {
        Result<T> result = new Result<T>();
        result.setCode(ResultEnum.SUCCESS).setData(data);
        return result;
    }

    public static <T> Result<T> fail(String msg) {
        Result<T> result = new Result<>();
        result.setCode(ResultEnum.FAIL).setMsg(msg);
        return result;
    }

    public static <T> Result<T> defineFail(Integer code, String msg) {
        Result<T> result = new Result<>();
        result.setCode(code).setMsg(msg);
        return result;
    }

    public static <T> Result<T> define(Integer code, String msg, T data) {
        Result<T> result = new Result<T>();
        result.setCode(code).setMsg(msg).setData(data);
        return result;
    }
}

