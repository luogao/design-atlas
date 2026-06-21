#!/usr/bin/env node
/**
 * 描述生成脚本 — 为每个设计系统生成 STYLE.md 描述性文字
 * 
 * 读取 tokens.css + preview.png，输出结构化描述 JSON
 * 之后用 Python 脚本把 JSON 合并到 STYLE.md
 * 
 * 用法: node collector/describe-all.js [--limit N]
 */
const fs = require('fs');
const path = require('path');

const ATLAS = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(ATLAS, 'manifest.json'), 'utf8'));

// 读取 token 文件，提取关键设计变量
function extractTokenSummary(sysId) {
  const tokenPath = path.join(ATLAS, 'systems', sysId, 'tokens.css');
  if (!fs.existsSync(tokenPath)) return '';
  const css = fs.readFileSync(tokenPath, 'utf8');
  
  // 提取所有 CSS 变量
  const vars = [];
  const regex = /--([\w-]+)\s*:\s*([^;]+);/g;
  let match;
  while ((match = regex.exec(css)) !== null) {
    vars.push('--' + match[1] + ': ' + match[2].trim());
  }
  return vars.join('\n');
}

// 为每个系统生成一个结构化描述对象
// 这个数据可以被 LLM 进一步丰富，也可以直接作为骨架
function generateDescription(sys) {
  const tokens = extractTokenSummary(sys.id);
  const palette = sys.palette || [];
  
  // 分析配色特征
  const colorTraits = analyzePalette(palette);
  // 分析 token 特征
  const tokenTraits = analyzeTokens(tokens);
  
  return {
    id: sys.id,
    name: sys.name,
    category: sys.category,
    year: sys.year,
    tags: sys.tags,
    one_liner: '', // 待 LLM 填充
    philosophy: '', // 待 LLM 填充
    color_analysis: colorTraits,
    token_analysis: tokenTraits,
    do_list: [], // 待 LLM 填充
    dont_list: [], // 待 LLM 填充
    best_for: [], // 待 LLM 填充
  };
}

function analyzePalette(palette) {
  if (!palette || palette.length === 0) return 'No palette defined';
  
  const traits = [];
  // 数量
  if (palette.length <= 2) traits.push('极简配色');
  else if (palette.length <= 4) traits.push('克制配色');
  else traits.push('丰富配色');
  
  // 亮度分析（简单近似）
  const dark = palette.filter(c => isDarkColor(c)).length;
  const light = palette.length - dark;
  if (dark > light * 2) traits.push('深色主导');
  else if (light > dark * 2) traits.push('浅色主导');
  else traits.push('明暗平衡');
  
  // 检查是否有饱和度高的颜色
  const vibrant = palette.some(c => isVibrant(c));
  if (vibrant) traits.push('含高饱和色');
  
  return traits.join('、');
}

function isDarkColor(hex) {
  const c = hex.replace('#', '');
  if (c.length !== 6) return false;
  const r = parseInt(c.substr(0, 2), 16);
  const g = parseInt(c.substr(2, 2), 16);
  const b = parseInt(c.substr(4, 2), 16);
  return (r * 0.299 + g * 0.587 + b * 0.114) < 128;
}

function isVibrant(hex) {
  const c = hex.replace('#', '');
  if (c.length !== 6) return false;
  const r = parseInt(c.substr(0, 2), 16);
  const g = parseInt(c.substr(2, 2), 16);
  const b = parseInt(c.substr(4, 2), 16);
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  return (max - min) > 100 && max > 150;
}

function analyzeTokens(tokens) {
  const traits = [];
  if (!tokens) return ['无 token 定义'];
  
  if (tokens.includes('border-radius') || tokens.includes('--radius')) {
    if (tokens.match(/radius.*0/) || tokens.includes('--radius: 0')) {
      traits.push('直角设计');
    } else if (tokens.match(/radius.*\d+/)) {
      traits.push('圆角设计');
    }
  }
  
  if (tokens.includes('box-shadow') || tokens.includes('--shadow')) {
    traits.push('使用阴影');
  }
  
  if (tokens.includes('monospace') || tokens.includes('Mono')) {
    traits.push('等宽字体');
  } else if (tokens.includes('serif')) {
    traits.push('衬线字体');
  } else if (tokens.includes('sans')) {
    traits.push('无衬线字体');
  }
  
  if (tokens.match(/gradient/i)) {
    traits.push('使用渐变');
  }
  
  if (tokens.match(/--gap|--spacing|--padding/i)) {
    traits.push('系统化间距');
  }
  
  return traits.length > 0 ? traits : ['基础 token'];
}

// Main
const args = process.argv.slice(2);
let limit = 0;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--limit' && args[i + 1]) limit = parseInt(args[i + 1]);
}

const systems = limit > 0 ? manifest.systems.slice(0, limit) : manifest.systems;
const descriptions = [];

console.log('Generating structural descriptions...');
for (const sys of systems) {
  const desc = generateDescription(sys);
  descriptions.push(desc);
  console.log('  ' + sys.id + ': ' + desc.color_analysis + ' / ' + desc.token_analysis.join('、'));
}

// 输出到 JSON
const outPath = path.join(ATLAS, 'collector', 'descriptions.json');
fs.writeFileSync(outPath, JSON.stringify(descriptions, null, 2));
console.log('\nWrote ' + descriptions.length + ' descriptions to ' + outPath);
console.log('Next step: Run describe-enrich.py to fill one_liner/philosophy with LLM');
