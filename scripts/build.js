/**
 * Cloudflare Pages 构建脚本：把根目录下的静态文件复制到 dist/ 目录。
 * - Pages 会在 dist/ 中寻找发布内容。
 * - 我们的项目是纯静态站点，因此只需把站点内容完整复制一份到 dist/ 即可。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'dist');

/** 需要复制的文件/目录（白名单） */
const INCLUDE = [
  'index.html',
  'courses.html',
  'course.html',
  'achievements.html',
  '404.html',
  'robots.txt',
  'favicon.svg',
  'README.md',
  'assets'
];

/** 递归复制目录或文件 */
function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      // 跳过以 . 开头的隐藏文件（例如 .git）
      if (name.startsWith('.')) continue;
      copyRecursive(path.join(src, name), path.join(dest, name));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function main() {
  console.log('[build] 开始构建输出目录:', OUT);

  // 清理旧的 dist/
  if (fs.existsSync(OUT)) {
    fs.rmSync(OUT, { recursive: true, force: true });
  }
  fs.mkdirSync(OUT, { recursive: true });

  let count = 0;
  for (const item of INCLUDE) {
    const src = path.join(ROOT, item);
    if (!fs.existsSync(src)) {
      console.log('[build] 跳过（不存在）:', item);
      continue;
    }
    copyRecursive(src, path.join(OUT, item));
    count += 1;
    console.log('[build] 已复制:', item);
  }

  console.log(`[build] 完成，共处理 ${count} 项，输出目录: dist/`);
  process.exit(0);
}

main();
