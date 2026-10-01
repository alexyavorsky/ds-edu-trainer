/** Компоненты, доступные во всех уроках без import (страница урока передаёт их в <Content components>). */
import AxisDiagram from '../reference/diagrams/AxisDiagram.astro';
import BroadcastDiagram from '../reference/diagrams/BroadcastDiagram.astro';
import ClassDiagram from '../reference/diagrams/ClassDiagram.astro';
import GroupbyDiagram from '../reference/diagrams/GroupbyDiagram.astro';
import MeltPivotDiagram from '../reference/diagrams/MeltPivotDiagram.astro';
import MergeDiagram from '../reference/diagrams/MergeDiagram.astro';
import MroDiagram from '../reference/diagrams/MroDiagram.astro';
import StackUnstackDiagram from '../reference/diagrams/StackUnstackDiagram.astro';
import Demo from './Demo.astro';
import Exercise from './Exercise.astro';
import Explain from './Explain.astro';
import Hint from './Hint.astro';
import Mistake from './Mistake.astro';
import Note from './Note.astro';
import Quiz from './Quiz.astro';

export const courseComponents = {
  Demo,
  Exercise,
  Hint,
  Quiz,
  Explain,
  Note,
  Mistake,
  AxisDiagram,
  BroadcastDiagram,
  ClassDiagram,
  GroupbyDiagram,
  MeltPivotDiagram,
  MergeDiagram,
  MroDiagram,
  StackUnstackDiagram,
};
