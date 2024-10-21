import { configureStore } from "@reduxjs/toolkit";
import { audioApi } from "@/services/api";


export const store = configureStore({
  reducer: {
    [audioApi.reducerPath]: audioApi.reducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
