<script setup lang="ts">
  import { useSlugify } from "~/composables/useSlugify";

  const { slugify } = useSlugify();

  const preview = ref<File | null>(null);
  const title = ref<string>("");
  const content = ref<string>("");
  const slug = ref<string>("");
  const isSlugEdited = ref(false);
  const categoryId = ref<number | null>(null);
  const categories = ref<{ id: number; name: string }[]>([]);

  onMounted(async () => {
    const res = (await $fetch("/api/v1/categories/")) as {
      items: { id: number; name: string }[];
    };
    categories.value = res.items;
  });

  watch(title, (val) => {
    if (!isSlugEdited.value) {
      slug.value = slugify(val);
    }
  });

  function onSlugInput() {
    isSlugEdited.value = true;
  }

  function onFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    let file: File | null = null;
    if (target.files && target.files.length > 0) {
      file = target.files[0] ?? null;
    }
    preview.value = file;
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();

    let previewPath = "";
    if (preview.value) {
      const formData = new FormData();
      formData.append("file", preview.value);
      const uploadRes = (await $fetch("/api/v1/news/upload-preview/", {
        method: "POST",
        body: formData,
      })) as { preview: string };
      previewPath = uploadRes.preview;
    }

    await $fetch("/api/v1/news/", {
      method: "POST",
      body: {
        title: title.value,
        content: content.value,
        preview: previewPath,
        slug: slug.value,
        category_id: categoryId.value,
      },
    });

    title.value = "";
    content.value = "";
    preview.value = null;
    slug.value = "";
    isSlugEdited.value = false;
    categoryId.value = null;
    alert("Новость добавлена!");
  }
</script>
<template>
  <div>
    <h1>Add News</h1>
    <NuxtLink to="/news">News</NuxtLink>
    <NuxtLink to="/news/categories/add">Add Category</NuxtLink>
    <div>
      <form @submit="handleSubmit">
        <div>
          <label for="preview">Preview</label>
          <input type="file" id="preview" @change="onFileChange" />
        </div>
        <div>
          <label for="title">Title</label>
          <input type="text" id="title" v-model="title" />
        </div>
        <div>
          <label for="slug">Slug</label>
          <input type="text" id="slug" v-model="slug" @input="onSlugInput" />
        </div>
        <div>
          <label for="content">Content</label>
          <textarea id="content" v-model="content"></textarea>
        </div>
        <div>
          <label for="category">Category</label>
          <select id="category" v-model="categoryId">
            <option :value="null" disabled>Выберите категорию</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <button type="submit">Add</button>
      </form>
    </div>
  </div>
</template>
