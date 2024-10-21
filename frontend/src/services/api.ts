import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const audioApi = createApi({
  reducerPath: 'audioApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost:5000' }),
  endpoints: (builder) => ({
    processAudio: builder.mutation<any, FormData>({
      query: (formData) => ({
        url: '/process_audio',
        method: 'POST',
        body: formData,
      }),
    }),
  }),
});

export const { useProcessAudioMutation } = audioApi;
