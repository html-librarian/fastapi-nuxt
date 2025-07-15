<script setup lang="ts">
  type News = {
    id: number;
    title: string;
    content: string;
    preview?: string | null;
    created_at?: string;
    updated_at?: string | null;
  };

  const news = ref<News[]>([]);
  const loading = ref(true);

  async function fetchNews() {
    loading.value = true;
    const res = (await $fetch("/api/v1/news/")) as { items: News[] };
    news.value = res.items;
    loading.value = false;
  }

  onMounted(fetchNews);
</script>

<template>
  <div>
    <h1>News</h1>
    <NuxtLink to="/news/add">Add News</NuxtLink>
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div v-if="news.length === 0">Новостей пока нет.</div>
      <ul v-else>
        <li v-for="item in news" :key="item.id">
          <div v-if="item.preview">
            <img
              :src="`/media/${item.preview}`"
              alt="preview"
              style="max-width: 100px; max-height: 100px"
            />
          </div>
          <strong>{{ item.title }}</strong>
          <div>{{ item.content }}</div>
          <small>Создано: {{ item.created_at }}</small>
        </li>
      </ul>
    </div>
  </div>
</template>
