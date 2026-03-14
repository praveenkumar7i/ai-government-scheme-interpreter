import { create } from "zustand";

type ChatState = {
  documentId: string;
  setDocumentId: (value: string) => void;
};

export const useChatStore = create<ChatState>((set) => ({
  documentId: "",
  setDocumentId: (value) => set({ documentId: value }),
}));
