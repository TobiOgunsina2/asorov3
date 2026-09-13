import type { components } from '@/api/generated';
import type { LessonViewModel } from '@/types/lesson-view-model';

type Lesson = components['schemas']['Lesson'];

interface LessonInteraction {
  selectedLessonId: number | null;
  hoveredLessonId: number | null;
}

export const createLessonViewModel = (
  lesson: Lesson,
  interaction: LessonInteraction,
): LessonViewModel => {
  return {
    lesson,

    isSelected:
      interaction.selectedLessonId === lesson.id,

    isHovered:
      interaction.hoveredLessonId === lesson.id,

    /**
     * These status checks depend on your actual API schema.
     * Adjust them to match your backend.
     */
    isLocked: false,
    isCompleted: false,
    isAvailable: true,
  };
};