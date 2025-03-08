#!/bin/bash
# Script to replace Element UI components with GlassUI components
echo "Replacing Element UI components with GlassUI components..."
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-button/<GlassButton/g" -e "s/<\/el-button>/<\/GlassButton>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-input/<GlassInput/g" -e "s/<\/el-input>/<\/GlassInput>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-select/<GlassSelect/g" -e "s/<\/el-select>/<\/GlassSelect>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-option/<GlassOption/g" -e "s/<\/el-option>/<\/GlassOption>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-dialog/<GlassDialog/g" -e "s/<\/el-dialog>/<\/GlassDialog>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-form/<GlassForm/g" -e "s/<\/el-form>/<\/GlassForm>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-form-item/<GlassFormItem/g" -e "s/<\/el-form-item>/<\/GlassFormItem>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-alert/<GlassAlert/g" -e "s/<\/el-alert>/<\/GlassAlert>/g" {} \;
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-tag/<GlassTag/g" -e "s/<\/el-tag>/<\/GlassTag>/g" {} \;
find frontend/src -type f -name "*.vue" -o -name "*.js" -o -name "*.ts" -exec sed -i "" -e "s/import { ElMessage } from 'element-plus';/import { GlassMessage } from '..\/components\/ui';/g" -e "s/ElMessage/GlassMessage/g" {} \;
echo "Replacement completed!"
