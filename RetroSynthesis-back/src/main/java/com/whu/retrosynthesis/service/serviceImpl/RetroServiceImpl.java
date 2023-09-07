package com.whu.retrosynthesis.service.serviceImpl;

import cn.hutool.core.util.StrUtil;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.whu.retrosynthesis.mapper.MoleculeMapper;
import com.whu.retrosynthesis.mapper.PathMapper;
import com.whu.retrosynthesis.mapper.UserMoleculeMapper;
import com.whu.retrosynthesis.pojo.Molecule;
import com.whu.retrosynthesis.pojo.Path;
import com.whu.retrosynthesis.pojo.Retro;
import com.whu.retrosynthesis.pojo.UserMolecule;
import com.whu.retrosynthesis.service.RetroService;
import com.whu.retrosynthesis.utils.UserHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;

import java.util.concurrent.TimeUnit;

import static com.whu.retrosynthesis.utils.RedisConstants.CACHE_RETRO_KEY;
import static com.whu.retrosynthesis.utils.RedisConstants.CACHE_RETRO_TTL;

@Service
public class RetroServiceImpl implements RetroService {
    @Autowired
    private RestTemplate restTemplate;
    @Autowired
    private MoleculeMapper moleculeMapper;
    @Autowired
    private UserMoleculeMapper userMoleculeMapper;
    @Autowired
    private PathMapper pathMapper;
    @Resource
    private StringRedisTemplate stringRedisTemplate;
    @Value("${flask.url}")
    private String flaskUrl;

    @Override
    public JSONObject planRoutes(Retro retro) {
        // target + key
        String target = retro.getTarget_mol();
        String retroKey = CACHE_RETRO_KEY + target;
        JSONObject resultJson;
        String redisResult = stringRedisTemplate.opsForValue().get(retroKey);
        // 如果redis不为空，直接返回
        if (StrUtil.isNotBlank(redisResult)){
            resultJson = JSONUtil.toBean(redisResult, JSONObject.class);
            return resultJson;
        }
        // 如果redis为空，调用接口
        String url = flaskUrl; // 替换为实际的URL
        try {
            resultJson = restTemplate.postForEntity(url, retro, JSONObject.class).getBody();
            assert resultJson != null;
            // 存储到redis
            stringRedisTemplate.opsForValue().set(retroKey, JSONUtil.toJsonStr(resultJson),CACHE_RETRO_TTL, TimeUnit.MINUTES);
            // 存储到数据库
            saveJsonData(resultJson);
        } catch (Exception e) {
            System.out.println(e);
            throw e;
        }
        return resultJson;
    }

    private void saveJsonData(JSONObject resultJson) {
        // molecule
        Molecule molecule = new Molecule();
        molecule.setSmiles(resultJson.getStr("target_mol"));
        molecule.setCid(resultJson.getInt("cid"));
        molecule.setBestLength(resultJson.getInt("best_length"));
        molecule.setBestPath(resultJson.getStr("best_route"));
        moleculeMapper.insert(molecule);
        // paths
        JSONArray field2Array = resultJson.getJSONArray("all_routes");
        String[] paths = field2Array.toArray(new String[0]);
        for (String s : paths) {
            Path path = new Path();
            path.setPath(s);
            path.setMoleculeId(molecule.getId());
            pathMapper.insert(path);
        }
        // userMolecule
        UserMolecule userMolecule = new UserMolecule();
        userMolecule.setUserId(UserHolder.getUser().getUid());
        userMolecule.setMoleculeId(molecule.getId());
        userMolecule.setExpansionTopk(resultJson.getInt("expansion_topk"));
        userMolecule.setIteration(resultJson.getInt("iteration"));
        userMolecule.setProcessingTime(resultJson.getFloat("excution_time"));
        userMolecule.setIsSuccess(Boolean.TRUE);
        userMoleculeMapper.insert(userMolecule);
    }
}
