'use client';

import React, { useMemo, useRef, useEffect } from 'react';
import Lesson from './Lesson';
import LessonPath from './LessonPath';

import type { components } from '@/api/generated';

import { useUnitInteraction } from '@/hooks/useUnitInteraction';
import {
  generateWindingLayout,
  calculateSpreadPosition,
  type Point,
} from '@/lib/lesson-layout';

type UnitType = components['schemas']['Unit'];

type Props = {
  unit: UnitType;
};

const ROW_HEIGHT = 15;

const DEFAULT_POSITION: Point = {
  x: 50,
  y: 0,
};

const Unit = ({ unit }: Props) => {
  const {
    selectedLessonId,
    toggleLessonSelection,
  } = useUnitInteraction();

  const lessonRefs = useRef<Record<number, HTMLDivElement | null>>({});

  useEffect(() => {
  if (selectedLessonId == null) return;

  requestAnimationFrame(() => {
    lessonRefs.current[selectedLessonId]?.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center",
    });
  });
}, [selectedLessonId]);

  /**
   * Generate base positions.
   */
  const lessonPositions = useMemo(() => {
    const generated =
      generateWindingLayout(unit.lessons.length, {
        leftX: 15,
        rightX: 57,
        rowSpacing: 1,
        startY: 0.5,
        organicOffset: 3,
      });

    const positions = new Map<number, Point>();

    unit.lessons.forEach((lesson, index) => {
      positions.set(
        lesson.id,
        generated[index] ?? DEFAULT_POSITION,
      );
    });

    return positions;
  }, [unit.lessons]);

  /**
   * Selected lesson's base position.
   */
  const selectedPosition =
    selectedLessonId !== null
      ? lessonPositions.get(selectedLessonId) ?? null
      : null;

  /**
   * Calculate final visual positions.
   */
  const positions = useMemo(() => {
    const result = new Map<number, Point>();

    unit.lessons.forEach((lesson) => {
      const originalPosition =
        lessonPositions.get(lesson.id) ??
        DEFAULT_POSITION;

      const isSelected =
        lesson.id === selectedLessonId;

      result.set(
        lesson.id,
        calculateSpreadPosition(
          originalPosition,
          selectedPosition,
          isSelected,
        ),
      );
    });

    return result;
  }, [
    unit.lessons,
    lessonPositions,
    selectedLessonId,
    selectedPosition,
  ]);

  /**
   * Convert positions to the array format
   * expected by LessonPath.
   */
  const pathPositions = useMemo(() => {
    return unit.lessons.map(
      (lesson) =>
        positions.get(lesson.id) ??
        DEFAULT_POSITION,
    );
  }, [unit.lessons, positions]);

  /**
   * Find selected lesson index for path styling.
   */
  const selectedIndex = useMemo(() => {
    if (selectedLessonId === null) {
      return null;
    }

    const index = unit.lessons.findIndex(
      (lesson) => lesson.id === selectedLessonId,
    );

    return index === -1 ? null : index;
  }, [unit.lessons, selectedLessonId]);

  const canvasHeight = Math.max(
    ROW_HEIGHT,
    unit.lessons.length * ROW_HEIGHT,
  );

  const canvasRows = Math.max(
    unit.lessons.length,
    1,
  );

  return (
    <section className="flex min-h-screen w-full snap-start flex-col pt-6">
      {/* Unit heading */}
      <header className="w-fit text-right">
        <p className="text-xl font-semibold text-gray-500">
          Unit {unit.id}
        </p>

        <h2 className="text-2xl font-bold text-black">
          {unit.title}
        </h2>
      </header>

      {/* Lesson path */}
      <div
        className="relative mt-6 w-full"
        style={{
          height: `${canvasHeight}rem`,
        }}
      >
        <LessonPath
          positions={pathPositions}
          selectedIndex={selectedIndex}
          height={canvasRows}
        />

        {unit.lessons.map((lesson) => {
          const isSelected =
            selectedLessonId === lesson.id;

          const position =
            positions.get(lesson.id) ??
            DEFAULT_POSITION;

          return (
            <div
              key={lesson.id}
              className={[
                'absolute cursor-pointer opacity-90',
                'transition-all duration-500 ease-out',
                'will-change-[left,top,width,height]',
                isSelected
                  ? 'z-20 h-[17rem] w-[min(27rem,90vw)] shadow-xl'
                  : 'z-10 h-[12rem] w-[12rem]',
              ].join(' ')}
              style={{
                left: `${position.x}%`,
                top: `${(position.y / canvasRows) * 100}%`,
                transform: 'translate(-50%, -50%)',
              }}
              ref={(element) => {
                lessonRefs.current[lesson.id] = element;
              }}
              onClick={() =>
                toggleLessonSelection(lesson.id)
              }
            >
              <Lesson
                isSelected={isSelected}
                lesson={lesson}
              />
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default Unit;