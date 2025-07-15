<script setup lang="ts">
  import { useSlugify } from "~/composables/useSlugify";

  const { slugify } = useSlugify();

  const name = ref("");
  const slug = ref("");
  const image = ref<File | null>(null);
  const isSlugEdited = ref(false);

  watch(name, (val) => {
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
    image.value = file;
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();

    let imagePath = "";
    if (image.value) {
      const formData = new FormData();
      formData.append("file", image.value);
      const uploadRes = (await $fetch("/api/v1/news/categories/upload-image/", {
        method: "POST",
        body: formData,
      })) as { image: string };
      imagePath = uploadRes.image;
    }

    await $fetch("/api/v1/categories/", {
      method: "POST",
      body: {
        name: name.value,
        slug: slug.value,
        image: imagePath,
      },
    });

    name.value = "";
    slug.value = "";
    image.value = null;
    isSlugEdited.value = false;
    alert("Категория добавлена!");
  }
</script>

<template>
  <div>
    <h1>Добавить категорию</h1>
    <NuxtLink to="/news/add">Добавить новость</NuxtLink>
    <form @submit="handleSubmit">
      <div>
        <label for="name">Название</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div>
        <label for="slug">Slug</label>
        <input
          type="text"
          id="slug"
          v-model="slug"
          @input="onSlugInput"
          required
        />
      </div>
      <div>
        <label for="image">Картинка</label>
        <input type="file" id="image" @change="onFileChange" />
      </div>
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>
