# GlassUI 组件库

GlassUI 是一个基于玻璃拟态设计的 Vue 3 组件库，旨在替代 Element Plus，提供更现代、更美观的 UI 体验。

## 安装和使用

GlassUI 已经集成到项目中，无需额外安装。在 `main.js` 中，我们已经注册了所有组件：

```js
import GlassUI from "./components/ui";
app.use(GlassUI);
```

## 组件替换指南

以下是 Element Plus 组件到 GlassUI 组件的替换指南：

### 按钮 (Button)

```vue
<!-- Element Plus -->
<el-button type="primary">按钮</el-button>

<!-- GlassUI -->
<GlassButton type="primary">按钮</GlassButton>
```

支持的属性：

- `type`: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
- `size`: 'small' | 'medium' | 'large'
- `disabled`: boolean
- `loading`: boolean
- `circle`: boolean

### 输入框 (Input)

```vue
<!-- Element Plus -->
<el-input v-model="input" placeholder="请输入"></el-input>

<!-- GlassUI -->
<GlassInput v-model="input" placeholder="请输入"></GlassInput>
```

支持的属性：

- `modelValue`: string | number
- `type`: string (如 'text', 'password' 等)
- `placeholder`: string
- `disabled`: boolean
- `required`: boolean
- `label`: string

### 选择器 (Select)

```vue
<!-- Element Plus -->
<el-select v-model="value" placeholder="请选择">
  <el-option value="option1" label="选项1"></el-option>
  <el-option value="option2" label="选项2"></el-option>
</el-select>

<!-- GlassUI -->
<GlassSelect v-model="value" placeholder="请选择">
  <GlassOption value="option1" label="选项1"></GlassOption>
  <GlassOption value="option2" label="选项2"></GlassOption>
</GlassSelect>
```

支持的属性：

- `modelValue`: string | number | boolean | array
- `options`: Array (可选，也可以使用 GlassOption 子组件)
- `placeholder`: string
- `disabled`: boolean
- `clearable`: boolean
- `label`: string

### 对话框 (Dialog)

```vue
<!-- Element Plus -->
<el-dialog v-model="visible" title="标题">
  内容
</el-dialog>

<!-- GlassUI -->
<GlassDialog
  :model-value="visible"
  @update:model-value="visible = $event"
  title="标题"
>
  内容
</GlassDialog>
```

支持的属性：

- `modelValue`: boolean
- `title`: string
- `width`: string
- `closeOnClickModal`: boolean
- `showClose`: boolean
- `modal`: boolean
- `appendToBody`: boolean

### 表单 (Form)

```vue
<!-- Element Plus -->
<el-form :model="form" label-width="120px">
  <el-form-item label="名称">
    <el-input v-model="form.name"></el-input>
  </el-form-item>
</el-form>

<!-- GlassUI -->
<GlassForm :model="form" label-width="120px">
  <GlassFormItem label="名称">
    <GlassInput v-model="form.name"></GlassInput>
  </GlassFormItem>
</GlassForm>
```

Form 支持的属性：

- `labelPosition`: 'top' | 'left' | 'right'
- `labelWidth`: string
- `model`: object
- `rules`: object

FormItem 支持的属性：

- `label`: string
- `prop`: string
- `required`: boolean
- `rules`: object | array
- `error`: string
- `labelWidth`: string

### 警告 (Alert)

```vue
<!-- Element Plus -->
<el-alert title="成功提示" type="success" show-icon></el-alert>

<!-- GlassUI -->
<GlassAlert title="成功提示" type="success" :show-icon="true"></GlassAlert>
```

支持的属性：

- `title`: string
- `type`: 'success' | 'warning' | 'info' | 'error'
- `description`: string
- `closable`: boolean
- `showIcon`: boolean
- `center`: boolean
- `effect`: 'light' | 'dark'

### 标签 (Tag)

```vue
<!-- Element Plus -->
<el-tag type="success">标签</el-tag>

<!-- GlassUI -->
<GlassTag type="success">标签</GlassTag>
```

支持的属性：

- `type`: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
- `closable`: boolean
- `size`: 'small' | 'medium' | 'large'
- `effect`: 'light' | 'dark'

### 消息提示 (Message)

```vue
<!-- Element Plus -->
import { ElMessage } from 'element-plus'; ElMessage.success('成功');

<!-- GlassUI -->
import { GlassMessage } from '@/components/ui'; GlassMessage.success('成功'); //
或者使用全局属性 this.$message.success('成功');
```

支持的方法：

- `GlassMessage.success(message)`
- `GlassMessage.warning(message)`
- `GlassMessage.info(message)`
- `GlassMessage.error(message)`
- `GlassMessage.closeAll()`

## 样式定制

GlassUI 使用 CSS 变量来定制样式，您可以在全局 CSS 中覆盖这些变量：

```css
:root {
  --text-color: rgba(255, 255, 255, 0.9);
  --glass-accent: #4fecb8;
  --glass-accent-secondary: #3a8ee6;
}
```

## 注意事项

1. GlassUI 组件使用 PascalCase 命名（如 `GlassButton`），而不是 kebab-case（如 `el-button`）。
2. 某些组件的属性名可能与 Element Plus 不完全相同，请参考上述文档。
3. GlassUI 组件设计为与玻璃拟态风格配合使用，在深色背景上效果最佳。
