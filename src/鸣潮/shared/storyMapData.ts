import type { StoryVersion } from './types';

/** 外部 WuWaShared 未提供时，由本仓库内置的剧情版本表（可随版本更新） */
export const FALLBACK_STORY_MAP: readonly StoryVersion[] = [
  {
    version: '1.0',
    parts: ['万象新声', '嘤鸣初相召', '撞金止行阵', '奔策候残星', '庭际刀刃鸣', '欲知天将雨', '千里卷戎旌'],
  },
  { version: '1.1', parts: ['往岁乘霄醒惊蛰'] },
  { version: '1.2', parts: ['天上月华人如愿'] },
  { version: '1.3', parts: ['行至海岸尽头'] },
  {
    version: '2.0',
    parts: ['如一叶小舟穿行于茫茫海洋', '那神圣微风时常吹入', '夜与昼，均请摘下面纱', '昔我悲伤，今却歌唱'],
  },
  { version: '2.1', parts: ['飞鸟轻鸣，浪涛欢唱'] },
  { version: '2.2', parts: ['圣者，忤逆者，告死者'] },
  { version: '2.3', parts: ['焰行夏曲庆团圆'] },
  { version: '2.4', parts: ['荣耀暗面', '燃烧的心'] },
  { version: '2.5', parts: ['捕梦于神秘园中', '铁锈，剑与烈阳'] },
  { version: '2.6', parts: ['灼我以烈阳', '今夜，注定属于月亮'] },
  { version: '2.7', parts: ['已逝的必将归来', '暗潮将映的黎明'] },
  { version: '2.8', parts: ['曙光停摆于荒地之上', '星光流转于眼眸之间'] },
  { version: '3.0', parts: ['未知的既感', '冰原下的星炬', '致第二次日出', '第三幕终'] },
  { version: '3.1', parts: ['远航星', '日光落处 (上)', '日光落处 (中)', '日光落处 (下)'] },
  { version: '3.2', parts: ['影下不落的黄金', '影面颠倒的兔影'] },
  {
    version: '3.3',
    parts: [
      '愿系铃中',
      '昨夜群星',
      '在熔解的夜空下 (上)',
      '在熔解的夜空下 (中)',
      '在熔解的夜空下 (下)',
    ],
  },
  {
    version: '3.4',
    parts: [
      '(简) 🌙边缘幻梦 (上)',
      '(简) 🌙边缘幻梦 (中)',
      '(简) 🌙边缘幻梦 (下)',
      '我们选择天空（上）',
      '我们选择天空（下）',
    ],
  },
  {
    version: '3.5',
    parts: ['遗音扶剑，荡梦而歌（上）', '遗音扶剑，荡梦而歌（中）', '遗音扶剑，荡梦而歌（下）'],
  },
];

/** 角色卡共享脚本尚未更新时，由本地补齐的章节 */
export const STORY_MAP_APPEND_PARTS: Record<string, readonly string[]> = {};

export function patchStoryMap(storyMap: readonly StoryVersion[]): StoryVersion[] {
  const inputMap = new Map(storyMap.map(v => [v.version, v]));
  const result: StoryVersion[] = [];

  // 以 FALLBACK_STORY_MAP 顺序遍历：输入中存在的版本合并 parts，不存在的直接追加
  for (const fb of FALLBACK_STORY_MAP) {
    const input = inputMap.get(fb.version);
    if (input) {
      // 合并：输入 parts 优先，追加 fallback 中不存在于输入的 parts
      const parts = [...input.parts];
      for (const p of fb.parts) {
        if (!parts.includes(p)) parts.push(p);
      }
      // 额外追加 STORY_MAP_APPEND_PARTS 中定义的章节
      const appendParts = STORY_MAP_APPEND_PARTS[fb.version];
      if (appendParts?.length) {
        for (const title of appendParts) {
          if (!parts.includes(title)) parts.push(title);
        }
      }
      result.push({ version: fb.version, parts });
      inputMap.delete(fb.version);
    } else {
      // 仅 fallback 中存在（如新增的 v3.4、v3.5）
      result.push({ ...fb, parts: [...fb.parts] });
    }
  }

  // 输入中存在但 fallback 中不存在的版本（如外部已更新的未来版本），追加到末尾
  for (const [, ver] of inputMap) {
    result.push({ ...ver, parts: [...ver.parts] });
  }

  return result;
}

export function getPatchedStoryMap(source: readonly StoryVersion[] = FALLBACK_STORY_MAP): StoryVersion[] {
  return patchStoryMap(source);
}
