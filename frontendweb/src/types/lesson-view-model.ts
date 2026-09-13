import type { components } from '@/api/generated';

export type Lesson = components['schemas']['Lesson'];

export interface LessonViewModel {
  lesson: Lesson;

  isSelected: boolean;
  isHovered: boolean;

  isLocked: boolean;
  isCompleted: boolean;
  isAvailable: boolean;
}