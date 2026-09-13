'use client';

import { useCallback, useState } from 'react';

export type LessonId = number;

interface UseUnitInteractionReturn {
  selectedLessonId: LessonId | null;
  hoveredLessonId: LessonId | null;

  isLessonSelected: (lessonId: LessonId) => boolean;
  isLessonHovered: (lessonId: LessonId) => boolean;

  selectLesson: (lessonId: LessonId) => void;
  clearSelection: () => void;
  toggleLessonSelection: (lessonId: LessonId) => void;

  setHoveredLesson: (lessonId: LessonId | null) => void;
}

export const useUnitInteraction = (): UseUnitInteractionReturn => {
  const [selectedLessonId, setSelectedLessonId] =
    useState<LessonId | null>(null);

  const [hoveredLessonId, setHoveredLessonId] =
    useState<LessonId | null>(null);

  /**
   * Select a lesson explicitly.
   */
  const selectLesson = useCallback((lessonId: LessonId) => {
    setSelectedLessonId(lessonId);
  }, []);

  /**
   * Clear the current selection.
   */
  const clearSelection = useCallback(() => {
    setSelectedLessonId(null);
  }, []);

  /**
   * Toggle selection.
   *
   * Clicking the selected lesson again
   * will deselect it.
   */
  const toggleLessonSelection = useCallback(
    (lessonId: LessonId) => {
      setSelectedLessonId((currentId) =>
        currentId === lessonId
          ? null
          : lessonId,
      );
    },
    [],
  );

  /**
   * Check whether a lesson is selected.
   */
  const isLessonSelected = useCallback(
    (lessonId: LessonId) =>
      selectedLessonId === lessonId,
    [selectedLessonId],
  );

  /**
   * Check whether a lesson is hovered.
   */
  const isLessonHovered = useCallback(
    (lessonId: LessonId) =>
      hoveredLessonId === lessonId,
    [hoveredLessonId],
  );

  return {
    selectedLessonId,
    hoveredLessonId,

    isLessonSelected,
    isLessonHovered,

    selectLesson,
    clearSelection,
    toggleLessonSelection,

    setHoveredLesson: setHoveredLessonId,
  };
};