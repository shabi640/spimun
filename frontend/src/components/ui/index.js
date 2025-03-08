import GlassButton from './GlassButton.vue';
import GlassInput from './GlassInput.vue';
import GlassSelect from './GlassSelect.vue';
import GlassOption from './GlassOption.vue';
import GlassDialog from './GlassDialog.vue';
import GlassForm from './GlassForm.vue';
import GlassFormItem from './GlassFormItem.vue';
import GlassAlert from './GlassAlert.vue';
import GlassTag from './GlassTag.vue';
import GlassMessage from './GlassMessage';
import GlassTable from './GlassTable.vue';
import GlassTableColumn from './GlassTableColumn.vue';
import GlassEmpty from './GlassEmpty.vue';
import GlassCollapse from './GlassCollapse.vue';
import GlassCollapseItem from './GlassCollapseItem.vue';
import GlassIcon from './GlassIcon.vue';
import GlassUpload from './GlassUpload.vue';
import GlassMenu from './GlassMenu.vue';
import GlassMenuItem from './GlassMenuItem.vue';
import GlassSubMenu from './GlassSubMenu.vue';
import GlassCheckbox from './GlassCheckbox.vue';
import GlassDrawer from './GlassDrawer.vue';
import GlassSkeleton from './GlassSkeleton.vue';

// 导出所有组件
export {
  GlassButton,
  GlassInput,
  GlassSelect,
  GlassOption,
  GlassDialog,
  GlassForm,
  GlassFormItem,
  GlassAlert,
  GlassTag,
  GlassMessage,
  GlassTable,
  GlassTableColumn,
  GlassEmpty,
  GlassCollapse,
  GlassCollapseItem,
  GlassIcon,
  GlassUpload,
  GlassMenu,
  GlassMenuItem,
  GlassSubMenu,
  GlassCheckbox,
  GlassDrawer,
  GlassSkeleton
};

// 创建插件安装方法
const GlassUI = {
  install(app) {
    app.component(GlassButton.name, GlassButton);
    app.component(GlassInput.name, GlassInput);
    app.component(GlassSelect.name, GlassSelect);
    app.component(GlassOption.name, GlassOption);
    app.component(GlassDialog.name, GlassDialog);
    app.component(GlassForm.name, GlassForm);
    app.component(GlassFormItem.name, GlassFormItem);
    app.component(GlassAlert.name, GlassAlert);
    app.component(GlassTag.name, GlassTag);
    app.component(GlassTable.name, GlassTable);
    app.component(GlassTableColumn.name, GlassTableColumn);
    app.component(GlassEmpty.name, GlassEmpty);
    app.component(GlassCollapse.name, GlassCollapse);
    app.component(GlassCollapseItem.name, GlassCollapseItem);
    app.component(GlassIcon.name, GlassIcon);
    app.component(GlassUpload.name, GlassUpload);
    app.component(GlassMenu.name, GlassMenu);
    app.component(GlassMenuItem.name, GlassMenuItem);
    app.component(GlassSubMenu.name, GlassSubMenu);
    app.component(GlassCheckbox.name, GlassCheckbox);
    app.component(GlassDrawer.name, GlassDrawer);
    app.component(GlassSkeleton.name, GlassSkeleton);
    
    // 添加全局属性
    app.config.globalProperties.$message = GlassMessage;
  }
};

export default GlassUI; 