# Jev Hub 部署与自动化手册

域名：`jev-ai.live`（Spaceship 注册）· 部署：Cloudflare Pages · 自动更新：GitHub Actions

## 一、推到 GitHub（一次性）

```bash
cd jev-hub
# 在 GitHub 网页上建一个空仓库（如 jev-hub，可 private），然后：
git remote add origin git@github.com:<你的用户名>/jev-hub.git
git push -u origin main
```

## 二、Cloudflare Pages 接管部署（一次性）

1. [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages → Create → Pages → Connect to Git**
2. 选刚推的 `jev-hub` 仓库，构建配置：
   - **Framework preset**: None
   - **Build command**: `python3 build.py`
   - **Build output directory**: `site`
3. Save and Deploy → 得到 `https://<项目名>.pages.dev` 预览地址，先确认能打开

> OG 图（og/ 目录）和新闻数据（data/news.json）都在仓库里，CF 构建机不需要装任何依赖。

## 三、Spaceship 绑定域名（一次性，推荐方案 A）

**方案 A（推荐）：DNS 交给 Cloudflare 管理（免费）**

1. Cloudflare 主页 → **Add a domain** → 输入 `jev-ai.live` → 选 **Free** 计划
2. Cloudflare 会给两个 nameserver（形如 `xxx.ns.cloudflare.com`）
3. Spaceship → 域名管理 → `jev-ai.live` → **Nameservers** → 改为 **Custom**，填上面两个 → 保存
   （生效几分钟到几小时，Spaceship 会显示 pending 状态）
4. 回到 Cloudflare Pages 项目 → **Custom domains → Set up a custom domain** → 输入 `jev-ai.live`
   DNS 已在 CF 名下，CNAME 记录自动添加，SSL 证书自动签发
5. 顺手把 `www.jev-ai.live` 也绑上并 301 到主域

**方案 B（不迁 DNS）：** 在 Spaceship 的 DNS 面板手动加记录：
- `CNAME` `www` → `<项目名>.pages.dev`
- `CNAME` `@` → `<项目名>.pages.dev`（Spaceship 若不支持根域 CNAME 扁平化，就用方案 A）

## 四、每日自动更新（全自动，无需手动上传）

链路：**GitHub Actions（每天北京时间 10:00）→ 跑 `update_news.py` 抓新闻 → 有更新就 commit `data/` 并 push → Cloudflare Pages 检测到 push → 自动跑 `build.py` 重新发布全站**（含 feed.xml）。

- 手动触发测试：GitHub 仓库 → Actions → daily-update → **Run workflow**
- 首次需在仓库 Settings → Actions → General → Allow all permissions（commit 推回需要）
- 通知：Actions 页可配置失败邮件提醒

## 五、本地改了内容怎么发

```bash
git add . && git commit -m "update content" && git push   # CF Pages 自动重建
# 若改了页面标题，还要重生成 OG 图（需 Pillow）：
/Users/alex/.workbuddy/binaries/python/envs/default/bin/python gen_og.py
```

## 六、收尾

- 部署成功后：Google Search Console → 添加资源 `jev-ai.live` → 提交 `sitemap.xml`
- 本地的每日定时任务迁移到 GitHub 后即可停用
