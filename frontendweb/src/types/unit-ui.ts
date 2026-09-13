export type LessonId = number;

export type LessonInteractionState =
  | 'idle'
  | 'hovered'
  | 'selected';

export interface UnitUIState {
  selectedLessonId: LessonId | null;
  hoveredLessonId: LessonId | null;
}

