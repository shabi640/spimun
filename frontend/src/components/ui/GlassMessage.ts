import { createVNode, render, Component, h } from 'vue';
import GlassAlert from './GlassAlert.vue';
import GlassDialog from './GlassDialog.vue';

interface MessageOptions {
  message?: string | number;
  type?: 'success' | 'warning' | 'info' | 'error';
  duration?: number;
  showClose?: boolean;
  center?: boolean;
  offset?: number;
  onClose?: () => void;
}

interface ConfirmOptions {
  title?: string;
  message: string;
  confirmButtonText?: string;
  cancelButtonText?: string;
  type?: 'success' | 'warning' | 'info' | 'error';
}

interface MessageInstance {
  id: string;
  vm: any;
}

interface MessageReturn {
  close: () => void;
}

interface MessageConstructor {
  (options: MessageOptions | string | number): MessageReturn;
  success: (options: MessageOptions | string | number) => MessageReturn;
  warning: (options: MessageOptions | string | number) => MessageReturn;
  info: (options: MessageOptions | string | number) => MessageReturn;
  error: (options: MessageOptions | string | number) => MessageReturn;
  closeAll: () => void;
  confirm: (message: string, title?: string, options?: any) => Promise<void>;
}

const instances: MessageInstance[] = [];
let seed = 1;

// Add a more comprehensive message deduplication system
let lastMessageType = '';
let lastMessageContent = '';
let lastMessageTime = 0;
let lastActionType = ''; // Track the type of action (e.g., 'publish', 'reject')
const DEBOUNCE_TIME = 1000; // 1 second debounce

// Function to identify the action type from message content
const getActionType = (type: string, content: string): string => {
  const lowerContent = content.toLowerCase();
  
  // Identify publish-related messages
  if (lowerContent.includes('publish') || lowerContent.includes('clause has been published')) {
    return 'publish';
  }
  
  // Identify reject-related messages
  if (lowerContent.includes('reject')) {
    return 'reject';
  }
  
  // Identify add-to-resolution-related messages
  if (lowerContent.includes('resolution')) {
    return 'resolution';
  }
  
  // Default: use the message content as the action type
  return content;
};

// Create a single function to handle message deduplication
const shouldShowMessage = (type: string, content: string): boolean => {
  const currentTime = Date.now();
  const actionType = getActionType(type, content);
  
  // If this is a message about the same action type and it's within the debounce time, ignore it
  if (actionType === lastActionType && 
      currentTime - lastMessageTime < DEBOUNCE_TIME) {
    console.log(`[GLASS_MESSAGE] Ignoring related ${type} message: "${content}" (same action: ${actionType})`);
    return false;
  }
  
  // If this is the exact same message and it's within the debounce time, ignore it
  if (type === lastMessageType && 
      content === lastMessageContent && 
      currentTime - lastMessageTime < DEBOUNCE_TIME) {
    console.log(`[GLASS_MESSAGE] Ignoring duplicate ${type} message: "${content}" (debounced)`);
    return false;
  }
  
  // Update last message tracking
  lastMessageType = type;
  lastMessageContent = content;
  lastMessageTime = currentTime;
  lastActionType = actionType;
  return true;
};

const GlassMessage = function(options: MessageOptions | string | number) {
  // 支持直接传入字符串作为选项
  if (typeof options === 'string' || typeof options === 'number') {
    options = {
      message: options
    };
  }
  
  const id = `message_${seed++}`;
  const container = document.createElement('div');
  
  // 处理 options
  const messageOptions: MessageOptions = {
    type: 'info',
    duration: 3000,
    showClose: false,
    ...options
  };
  
  // 处理垂直偏移量
  let verticalOffset = messageOptions.offset || 20;
  instances.forEach(({ vm }) => {
    verticalOffset += (vm.el.offsetHeight || 0) + 16;
  });
  messageOptions.offset = verticalOffset;
  
  // 创建关闭函数
  const userOnClose = messageOptions.onClose;
  
  const close = () => {
    const idx = instances.findIndex(instance => instance.id === id);
    if (idx === -1) return;
    
    const { vm } = instances[idx];
    if (!vm) return;
    
    userOnClose && userOnClose();
    
    const removedHeight = vm.el.offsetHeight;
    render(null, container);
    document.body.removeChild(container);
    
    // 调整其他消息的位置
    instances.splice(idx, 1);
    const len = instances.length;
    if (len < 1) return;
    
    for (let i = idx; i < len; i++) {
      const pos = parseInt(instances[i].vm.el.style.top) - removedHeight - 16;
      instances[i].vm.component.props.offset = pos;
    }
  };
  
  // 创建清除定时器的函数
  let timer: number | null = null;
  
  const clearTimer = () => {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  };
  
  function startTimer() {
    if (messageOptions.duration && messageOptions.duration > 0) {
      timer = window.setTimeout(() => {
        close();
      }, messageOptions.duration);
    }
  }
  
  // 创建 VNode
  const vnode = createVNode(GlassAlert as Component, {
    ...messageOptions,
    type: messageOptions.type,
    title: messageOptions.message,
    closable: messageOptions.showClose,
    center: messageOptions.center,
    onClose: close,
    style: {
      position: 'fixed',
      top: `${messageOptions.offset}px`,
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 9999,
      width: 'auto',
      minWidth: '300px',
      maxWidth: '80%',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
    }
  });
  
  // 添加鼠标悬停事件处理
  vnode.props!.onMouseenter = clearTimer;
  vnode.props!.onMouseleave = startTimer;
  
  // 渲染并挂载
  render(vnode, container);
  document.body.appendChild(container);
  
  // 设置定时关闭
  startTimer();
  
  // 保存实例
  const instance: MessageInstance = {
    id,
    vm: vnode
  };
  
  instances.push(instance);
  
  // 返回关闭方法供外部使用
  return {
    close
  };
} as MessageConstructor;

// 添加快捷方法
['success', 'warning', 'info', 'error'].forEach(type => {
  (GlassMessage as any)[type] = (options: MessageOptions | string | number) => {
    console.log(`[GLASS_MESSAGE] Attempting to show ${type} message:`, options);
    
    // Extract the message content
    const messageContent = typeof options === 'string' || typeof options === 'number' 
      ? options.toString() 
      : options.message?.toString() || '';
    
    // Check if we should show this message
    if (!shouldShowMessage(type, messageContent)) {
      return { close: () => {} }; // Return dummy close function
    }
    
    console.log(`[GLASS_MESSAGE] Showing ${type} message: "${messageContent}"`);
    
    if (typeof options === 'string' || typeof options === 'number') {
      options = {
        message: options
      };
    }
    (options as MessageOptions).type = type as 'success' | 'warning' | 'info' | 'error';
    return GlassMessage(options);
  };
});

// 关闭所有消息
GlassMessage.closeAll = () => {
  instances.forEach(instance => {
    instance.vm.component.props.onClose();
  });
};

// Add confirm method
GlassMessage.confirm = function(message: string, title: string = 'Confirm', options: any = {}): Promise<void> {
  return new Promise((resolve, reject) => {
    const container = document.createElement('div');
    
    const handleConfirm = () => {
      render(null, container);
      document.body.removeChild(container);
      resolve();
    };
    
    const handleCancel = () => {
      render(null, container);
      document.body.removeChild(container);
      reject(new Error('User cancelled'));
    };
    
    const vnode = createVNode(GlassDialog, {
      modelValue: true,
      title: title,
      'onUpdate:modelValue': (val: boolean) => {
        if (!val) handleCancel();
      },
      width: '400px'
    }, {
      default: () => h('div', { style: { textAlign: 'center' } }, message),
      footer: () => [
        h('button', {
          class: 'glass-button glass-button--default',
          onClick: handleCancel,
          style: { marginRight: '10px' }
        }, options.cancelButtonText || 'Cancel'),
        h('button', {
          class: `glass-button glass-button--${options.type || 'primary'}`,
          onClick: handleConfirm
        }, options.confirmButtonText || 'Confirm')
      ]
    });
    
    render(vnode, container);
    document.body.appendChild(container);
  });
};

export default GlassMessage; 