# patch_phone_pagination.py
# 将此脚本与 index.js 放在同一目录下运行：python patch_phone_pagination.py

import re

with open('index.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"原始文件大小: {len(content)} 字符")

# ========== 1. 在聊天面板插入翻页导航栏 ==========
old_chat_header = '''<div class="chat-header">
                                    <button class="back-button" id="chat-back-btn">
                                        <i class="fas fa-chevron-left"></i>
                                    </button>
                                    <span class="app-title" id="chat-title" style="flex: 1;">聊天</span>
                                    <div id="chat-right-actions" style="width: 36px; flex-shrink: 0;"></div>
                                </div>
                                <div class="chat-messages" id="chat-messages">'''

new_chat_header = '''<div class="chat-header">
                                    <button class="back-button" id="chat-back-btn">
                                        <i class="fas fa-chevron-left"></i>
                                    </button>
                                    <span class="app-title" id="chat-title" style="flex: 1;">聊天</span>
                                    <div id="chat-right-actions" style="width: 36px; flex-shrink: 0;"></div>
                                </div>
                                <div id="chat-page-nav" style="display:none;height:40px;align-items:center;justify-content:space-between;padding:0 12px;background:rgba(255,255,255,0.95);border-bottom:1px solid rgba(0,0,0,0.1);">
                                    <button id="page-prev" style="background:none;border:none;color:#667eea;font-size:16px;cursor:pointer;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:all 0.2s;"><i class="fas fa-chevron-left"></i></button>
                                    <span id="page-indicator" style="font-size:12px;color:#666;font-weight:600;">0 / 0</span>
                                    <button id="page-next" style="background:none;border:none;color:#667eea;font-size:16px;cursor:pointer;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:all 0.2s;"><i class="fas fa-chevron-right"></i></button>
                                </div>
                                <div class="chat-messages" id="chat-messages">'''

if old_chat_header in content:
    content = content.replace(old_chat_header, new_chat_header)
    print("✅ 已插入翻页导航栏")
else:
    print("⚠️ 未找到聊天面板头部，跳过导航栏插入")

# ========== 2. 在 messageSender 类后插入分页状态管理 ==========
old_msend = '};let De=null,Ve=null,Ue=null,Re=!1;'
new_msend = '''};
window.phoneChatHistory={};
window.getPhoneChatState=function(e){return window.phoneChatHistory[e]||(window.phoneChatHistory[e]={pages:[],currentIndex:0,maxPages:10}),window.phoneChatHistory[e]};
window.renderPhonePages=function(){const e=window.getPhoneChatState(Ve),n=e.pages[e.currentIndex],t=c("#chat-messages");if(!n)return t.html('<div style="text-align:center;padding:40px;color:#9ca3af;">暂无消息</div>'),void window.updatePageNav(e);let o="";if(n.userMsg&&(o+=`<div class="message-item mine"><div class="message-bubble"><div style="font-size:11px;color:#4CAF50;font-weight:600;margin-bottom:4px;text-align:right;">我</div><div>${qe(n.userMsg)}</div><div class="message-time" style="text-align:right;">${n.userTime||""}</div></div></div>`),n.aiMsg){const t=V(Ue)||"",a=t?`<img src="${t}" style="width:36px;height:36px;border-radius:8px;object-fit:cover;flex-shrink:0;" onerror="this.style.display='none'">`:`<div style="width:36px;height:36px;border-radius:8px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:14px;flex-shrink:0;">${(Ue||"?").charAt(0)}</div>`;o+=`<div class="message-item other" style="display:flex;align-items:flex-start;gap:8px;">${a}<div class="message-bubble"><div style="font-size:11px;color:#2196F3;font-weight:600;margin-bottom:4px;">${Ue||"AI"}</div><div>${qe(n.aiMsg)}</div><div class="message-time">${n.aiTime||""}</div></div></div>`}else if(n.pending){const t=V(Ue)||"",a=t?`<img src="${t}" style="width:36px;height:36px;border-radius:8px;object-fit:cover;flex-shrink:0;" onerror="this.style.display='none'">`:`<div style="width:36px;height:36px;border-radius:8px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:14px;flex-shrink:0;">${(Ue||"?").charAt(0)}</div>`;o+=`<div class="message-item other" style="display:flex;align-items:flex-start;gap:8px;">${a}<div class="message-bubble"><div style="font-size:11px;color:#2196F3;font-weight:600;margin-bottom:4px;">${Ue||"AI"}</div><div style="opacity:0.6;"><i class="fas fa-spinner fa-spin"></i> 生成中...</div></div></div>`}t.html(o),window.updatePageNav(e)};
window.updatePageNav=function(e){const n=c("#page-indicator");n.length&&n.text(`${e.currentIndex+1} / ${e.pages.length}`);const t=c("#page-prev"),o=c("#page-next");t.length&&t.prop("disabled",e.currentIndex<=0).css("opacity",e.currentIndex<=0?0.3:1),o.length&&o.prop("disabled",e.currentIndex>=e.pages.length-1).css("opacity",e.currentIndex>=e.pages.length-1?0.3:1)};
let De=null,Ve=null,Ue=null,Re=!1;'''

if old_msend in content:
    content = content.replace(old_msend, new_msend)
    print("✅ 已插入分页状态管理")
else:
    print("⚠️ 未找到 messageSender 类结束标记，跳过状态管理插入")

# ========== 3. 修改 We()：打开聊天时显示翻页栏 ==========
old_we = '''function We(e,n,t=!1,o=''){Ve=e,Ue=n,Re=t,window.messageSender.setCurrentChat(e,n,t);let a=t?`👥 ${n}`:`💬 ${n}`;if(t&&o){a+=` (${o.split(/[、,，]/).filter(e=>e.trim()).length}人)`,c('#chat-title').html(`\n            <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;">\n                <div style="font-size: 16px; font-weight: 600;">${a}</div>\n                <div style="font-size: 11px; opacity: 0.7; margin-top: 2px;">${o}</div>\n            </div>\n        `)}else c('#chat-title').text(a);const i=c('#chat-right-actions');t?i.html(`\n            <button class="chat-group-more-btn" data-group-id="${e}" data-group-name="${n}" data-group-members="${o}"\n                    style="background: none; border: none; color: #6b7280; font-size: 22px;\n                           cursor: pointer; padding: 0; width: 36px; height: 36px; display: flex;\n                           align-items: center; justify-content: center; transition: all 0.2s;"\n                    onmouseover="this.style.color='#374151'; this.style.transform='scale(1.1)'"\n                    onmouseout="this.style.color='#6b7280'; this.style.transform='scale(1)'"\n                    title="群聊管理">\n                <i class="fas fa-ellipsis-v"></i>\n            </button>\n        `):i.html(''),Fe(e,t),c('#phone-chat-panel').addClass('active'),c('#chat-input').val(''),De&&clearInterval(De),De=setInterval(()=>{const n=r().hasClass('active'),o=c('#phone-chat-panel').hasClass('active');n&&o&&Fe(e,t)},1e3)}'''

new_we = '''function We(e,n,t=!1,o=''){Ve=e,Ue=n,Re=t,window.messageSender.setCurrentChat(e,n,t);let a=t?`👥 ${n}`:`💬 ${n}`;if(t&&o){a+=` (${o.split(/[、,，]/).filter(e=>e.trim()).length}人)`,c('#chat-title').html(`\n            <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;">\n                <div style="font-size: 16px; font-weight: 600;">${a}</div>\n                <div style="font-size: 11px; opacity: 0.7; margin-top: 2px;">${o}</div>\n            </div>\n        `)}else c('#chat-title').text(a);const i=c('#chat-right-actions');t?i.html(`\n            <button class="chat-group-more-btn" data-group-id="${e}" data-group-name="${n}" data-group-members="${o}"\n                    style="background: none; border: none; color: #6b7280; font-size: 22px;\n                           cursor: pointer; padding: 0; width: 36px; height: 36px; display: flex;\n                           align-items: center; justify-content: center; transition: all 0.2s;"\n                    onmouseover="this.style.color='#374151'; this.style.transform='scale(1.1)'"\n                    onmouseout="this.style.color='#6b7280'; this.style.transform='scale(1)'"\n                    title="群聊管理">\n                <i class="fas fa-ellipsis-v"></i>\n            </button>\n        `):i.html(''),c('#chat-page-nav').css('display','flex'),Fe(e,t),c('#phone-chat-panel').addClass('active'),c('#chat-input').val(''),De&&clearInterval(De),De=setInterval(()=>{const n=r().hasClass('active'),o=c('#phone-chat-panel').hasClass('active');n&&o&&Fe(e,t)},1e3)}'''

if old_we in content:
    content = content.replace(old_we, new_we)
    print("✅ 已修改 We()")
else:
    print("⚠️ 未找到 We()，跳过")

# ========== 4. 修改 Ge()：关闭聊天时隐藏翻页栏 ==========
old_ge = "function Ge(){c('#phone-chat-panel').removeClass('active'),window.messageSender.clearCurrentChat(),De&&(clearInterval(De),De=null)}"
new_ge = "function Ge(){c('#phone-chat-panel').removeClass('active'),c('#chat-page-nav').css('display','none'),window.messageSender.clearCurrentChat(),De&&(clearInterval(De),De=null)}"

if old_ge in content:
    content = content.replace(old_ge, new_ge)
    print("✅ 已修改 Ge()")
else:
    print("⚠️ 未找到 Ge()，跳过")

# ========== 5. 替换 Fe() 为分页渲染入口 ==========
fe_start = content.find('function Fe(e,n){')
he_start = content.find('function He(){')
if fe_start != -1 and he_start != -1 and fe_start < he_start:
    old_fe = content[fe_start:he_start]
    new_fe = 'function Fe(e,n){window.renderPhonePages&&window.renderPhonePages()}\n'
    content = content.replace(old_fe, new_fe)
    print("✅ 已替换 Fe() 为分页渲染")
else:
    print("⚠️ 未定位到 Fe() 范围，跳过")

# ========== 6. 替换 He() 为分页发送逻辑 ==========
old_he = 'function He(){const e=c("#chat-input");if(!e.length)return;const n=e.val();if(!n||!n.trim())return e.val(""),void e.focus();const t=n.trim();e.val(""),window.messageSender.sendMessage(t).then(e=>{e||("undefined"!=typeof toastr&&toastr.error("发送失败"),e.val(t))}).catch(e=>{console.error(e),"undefined"!=typeof toastr&&toastr.error("发送失败: "+e.message)})}'

new_he = '''function He(){const e=c("#chat-input");if(!e.length)return;const n=e.val();if(!n||!n.trim())return e.val(""),void e.focus();if(!Ve)return void("undefined"!=typeof toastr&&toastr.error("请选择一个聊天对象"));const t=n.trim();e.val("");const o=window.getPhoneChatState(Ve);if(o.currentIndex<o.pages.length-1&&(o.pages=o.pages.slice(0,o.currentIndex+1)),o.pages.length>=o.maxPages){o.pages.shift();let e=o.currentIndex-1;o.currentIndex=e<0?0:e}o.pages.push({userMsg:t,aiMsg:"",userTime:new Date().toLocaleTimeString("zh-CN",{hour:"2-digit",minute:"2-digit"}),aiTime:"",pending:!0}),o.currentIndex=o.pages.length-1,window.renderPhonePages(),window.messageSender.sendMessage(t).then(e=>{e||("undefined"!=typeof toastr&&toastr.error("发送失败"),c("#chat-input").val(t))}).catch(e=>{console.error(e),"undefined"!=typeof toastr&&toastr.error("发送失败: "+e.message)})}'''

if old_he in content:
    content = content.replace(old_he, new_he)
    print("✅ 已替换 He()")
else:
    print("⚠️ 未找到 He()，跳过")

# ========== 7. 修改 sendViaGenerate：AI 回复后写入当前页 ==========
old_sendvia = '''async sendViaGenerate(e){const n=this.resolveTavernHelperWindow();if(!n)throw new Error("TavernHelper.generate 不可用，请确认已启用酒馆助手");const t=n.TavernHelper;await t.createChatMessages([{role:"user",message:e}]);const o=await t.generate({user_input:e,max_chat_history:40,should_silence:!0}),a="string"==typeof o?o:o?.content??"";return a.trim()&&await t.createChatMessages([{role:"assistant",message:a}]),!0}'''

new_sendvia = '''async sendViaGenerate(e){const n=this.resolveTavernHelperWindow();if(!n)throw new Error("TavernHelper.generate 不可用，请确认已启用酒馆助手");const t=n.TavernHelper;await t.createChatMessages([{role:"user",message:e}]);const o=await t.generate({user_input:e,max_chat_history:40,should_silence:!0}),a="string"==typeof o?o:o?.content??"";if(a.trim()){await t.createChatMessages([{role:"assistant",message:a}]);const e=window.getPhoneChatState(this.currentFriendId);e&&e.pages[e.currentIndex]&&(e.pages[e.currentIndex].aiMsg=a,e.pages[e.currentIndex].aiTime=new Date().toLocaleTimeString("zh-CN",{hour:"2-digit",minute:"2-digit"}),e.pages[e.currentIndex].pending=!1,window.renderPhonePages&&window.renderPhonePages())}return!0}'''

if old_sendvia in content:
    content = content.replace(old_sendvia, new_sendvia)
    print("✅ 已修改 sendViaGenerate")
else:
    print("⚠️ 未找到 sendViaGenerate，跳过")

# ========== 8. 绑定翻页按钮事件 ==========
old_bind = "c('#chat-send-btn').off('click.wuwaPhone').on('click.wuwaPhone',function(){He()}),c('#chat-input').off('keypress.wuwaPhone').on('keypress.wuwaPhone',function(e){'Enter'!==e.key||e.shiftKey||(e.preventDefault(),He())})"
new_bind = "c('#chat-send-btn').off('click.wuwaPhone').on('click.wuwaPhone',function(){He()}),c('#chat-input').off('keypress.wuwaPhone').on('keypress.wuwaPhone',function(e){'Enter'!==e.key||e.shiftKey||(e.preventDefault(),He())}),c('#page-prev').off('click.wuwaPhone').on('click.wuwaPhone',function(){const e=window.getPhoneChatState(Ve);e.currentIndex>0&&(e.currentIndex--,window.renderPhonePages())}),c('#page-next').off('click.wuwaPhone').on('click.wuwaPhone',function(){const e=window.getPhoneChatState(Ve);e.currentIndex<e.pages.length-1&&(e.currentIndex++,window.renderPhonePages())})"

if old_bind in content:
    content = content.replace(old_bind, new_bind)
    print("✅ 已绑定翻页按钮事件")
else:
    print("⚠️ 未找到事件绑定点，跳过")

# ========== 9. 酒馆主界面消息隐藏器 ==========
hider_code = ''';function installTavernMessageHider(){if(window.__phoneTavernHiderInstalled)return;window.__phoneTavernHiderInstalled=!0;const e=document.createElement("style");e.textContent=".mes[data-phone-msg=true]{display:none!important}",document.head.appendChild(e);const n=new MutationObserver(()=>{document.querySelectorAll(".mes").forEach(e=>{const n=e.querySelector(".mes_text");if(n){const t=n.textContent||"";/\\[(我方消息|对方消息|群聊消息|群聊|创建群聊|我方群聊消息)/.test(t)&&e.setAttribute("data-phone-msg","true")}})});const t=document.getElementById("chat");t&&n.observe(t,{childList:!0,subtree:!0})}installTavernMessageHider();'''
content = content + hider_code
print("✅ 已追加酒馆消息隐藏器")

# 保存
with open('index.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n🎉 修改完成！新文件大小: {len(content)} 字符")
print("请刷新你的 SillyTavern 页面以生效。")
print("\n使用说明：")
print("- 发送消息后会在最后一页新增一页（用户消息 + AI回复）")
print("- 最多保留 10 页，超过后自动移除最早的一页")
print("- 点击左右箭头可翻页浏览历史对话")
print("- 酒馆主界面的对应消息会被自动隐藏，仅在此手机页面显示")