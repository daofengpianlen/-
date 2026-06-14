# 鸣潮 · 伪同层前端（CDN 部署）

本仓库为 **SillyTavern + 酒馆助手** 用的鸣潮 GAL 伪同层脚本，托管于 jsDelivr，**无需本地 `pnpm serve:dist`**。

## CDN 根地址

```
https://cdn.jsdelivr.net/gh/daofengpianlen/-/main
```

## 导入酒馆

在角色卡 → 脚本 → 导入以下 JSON（见 `导入到酒馆中/`）：

| 脚本 | 说明 |
|------|------|
| 鸣潮共享 | STORY_MAP / 剧情逻辑 |
| 鸣潮变量结构 | MVU schema |
| 鸣潮开场 | 第 0 楼开场面板 |
| **鸣潮伪同层** | GAL 主界面 + 小爱手机 |

也可直接在脚本内容里写：

```javascript
import 'https://cdn.jsdelivr.net/gh/daofengpianlen/-/main/dist/鸣潮/%E8%84%9A%E6%9C%AC/%E4%BC%AA%E5%90%8C%E5%B1%82/index.js'
```

## CG / 本地资源

- 本仓库默认只含 **脚本** 与 **资源索引 JSON**（`cgSceneIndex.json`、`mediaLocalMap.json`）。
- 未上传 `dist/鸣潮/assets/cg/` 时，CG 会回退到 **catbox** 远程 URL（见 `mediaLocalMap.json`）。
- 若需 CDN 本地 CG：将 `assets/cg` 一并放入本仓库（体积较大，建议 Git LFS）或自建静态站，脚本会通过 `import.meta.url` 自动解析 `…/assets/` 路径。

## 开发

源码在 [tavern_helper_template](https://github.com/) 项目的 `src/鸣潮/`。修改后在本仓库根目录执行：

```bash
# 在模板项目内
node src/鸣潮/工具/packageWuwaDeploy.mjs --cdn-base=https://cdn.jsdelivr.net/gh/daofengpianlen/-/main
```

然后提交 `release/wuwa-cdn` 目录内容到本仓库 `main` 分支。

## 伪同层显示

- iframe 固定挂在 **第 0 楼**；有 `<gal>` 后内容读最新 gal 楼。
- 控制台：`__WUWA_DEBUG_HUB__()`、`__WUWA_REMOUNT_HUB__()`
