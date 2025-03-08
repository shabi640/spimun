# Element Plus Migration Guide

This document provides instructions for completing the migration from Element Plus to our custom GlassUI components.

## Current Status

We have already:

1. Created custom GlassUI components for basic UI elements (buttons, inputs, selects, dialogs, forms, alerts, tags, messages)
2. Removed Element Plus from package.json
3. Removed Element Plus from Vite configuration
4. Replaced many Element Plus components with GlassUI equivalents
5. Updated import statements to use GlassUI components

## Remaining Tasks

### 1. Replace Complex Components

The following Element Plus components still need custom GlassUI replacements:

#### Tables (`el-table`, `el-table-column`)

Create custom table components:

- `GlassTable.vue`
- `GlassTableColumn.vue`

Example usage:

```vue
<!-- Before -->
<el-table :data="data">
  <el-table-column prop="name" label="Name" />
</el-table>

<!-- After -->
<GlassTable :data="data">
  <GlassTableColumn prop="name" label="Name" />
</GlassTable>
```

#### Empty State (`el-empty`)

Create a custom empty state component:

- `GlassEmpty.vue`

Example usage:

```vue
<!-- Before -->
<el-empty description="No data" />

<!-- After -->
<GlassEmpty description="No data" />
```

#### Collapse (`el-collapse`, `el-collapse-item`)

Create custom collapse components:

- `GlassCollapse.vue`
- `GlassCollapseItem.vue`

Example usage:

```vue
<!-- Before -->
<el-collapse v-model="activeNames">
  <el-collapse-item name="1" title="Title">
    Content
  </el-collapse-item>
</el-collapse>

<!-- After -->
<GlassCollapse v-model="activeNames">
  <GlassCollapseItem name="1" title="Title">
    Content
  </GlassCollapseItem>
</GlassCollapse>
```

#### Icons (`el-icon`)

Create a custom icon system or use a different icon library:

- `GlassIcon.vue`

Example usage:

```vue
<!-- Before -->
<el-icon><ChatLineRound /></el-icon>

<!-- After -->
<GlassIcon name="chat" />
```

### 2. Update Component References

After creating the new components, update all references in the codebase:

```bash
# Replace table components
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-table/<GlassTable/g" -e "s/<\/el-table>/<\/GlassTable>/g" -e "s/<el-table-column/<GlassTableColumn/g" -e "s/<\/el-table-column>/<\/GlassTableColumn>/g" {} \;

# Replace empty component
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-empty/<GlassEmpty/g" -e "s/<\/el-empty>/<\/GlassEmpty>/g" {} \;

# Replace collapse components
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-collapse/<GlassCollapse/g" -e "s/<\/el-collapse>/<\/GlassCollapse>/g" -e "s/<el-collapse-item/<GlassCollapseItem/g" -e "s/<\/el-collapse-item>/<\/GlassCollapseItem>/g" {} \;

# Replace icon component
find frontend/src -type f -name "*.vue" -exec sed -i "" -e "s/<el-icon/<GlassIcon/g" -e "s/<\/el-icon>/<\/GlassIcon>/g" {} \;
```

### 3. Clean Up CSS References

Remove any Element Plus specific CSS classes and styles:

```bash
# Find Element Plus CSS classes
grep -r "el-" --include="*.vue" --include="*.css" frontend/src
```

Replace these with your custom GlassUI classes.

### 4. Update Import Statements

Make sure all import statements are updated:

```bash
# Find remaining Element Plus imports
grep -r "element-plus" --include="*.vue" --include="*.js" --include="*.ts" frontend/src
```

### 5. Testing

After completing the migration:

1. Test all components to ensure they function correctly
2. Check for any styling issues
3. Verify that there are no console errors related to missing Element Plus components
4. Run the application in development mode to catch any runtime errors

## Additional Resources

- [GlassUI Component Documentation](./README.md)
- [Vue 3 Custom Component Guide](https://vuejs.org/guide/components/registration.html)
