import { create } from 'zustand';

interface Resume {
  id: number;
  filename: string;
  file_path: string;
  is_processed: boolean;
  ats_score?: number;
  created_at: string;
}

interface ResumeState {
  resumes: Resume[];
  selectedResume: Resume | null;
  isLoading: boolean;
  error: string | null;
  setResumes: (resumes: Resume[]) => void;
  setSelectedResume: (resume: Resume | null) => void;
  setIsLoading: (value: boolean) => void;
  setError: (error: string | null) => void;
  addResume: (resume: Resume) => void;
  removeResume: (id: number) => void;
}

export const useResumeStore = create<ResumeState>((set) => ({
  resumes: [],
  selectedResume: null,
  isLoading: false,
  error: null,

  setResumes: (resumes) => set({ resumes }),
  setSelectedResume: (resume) => set({ selectedResume: resume }),
  setIsLoading: (value) => set({ isLoading: value }),
  setError: (error) => set({ error }),

  addResume: (resume) =>
    set((state) => ({
      resumes: [resume, ...state.resumes],
    })),

  removeResume: (id) =>
    set((state) => ({
      resumes: state.resumes.filter((r) => r.id !== id),
    })),
}));
