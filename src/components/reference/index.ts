/** Компоненты, доступные во всех статьях справочника без import (передаются странице статьи в <Content components>). */
import Example from './Example.astro';
import Params from './Params.astro';
import Pitfall from './Pitfall.astro';
import Setup from './Setup.astro';
import Syntax from './Syntax.astro';
import VersionNote from './VersionNote.astro';
import AxisDiagram from './diagrams/AxisDiagram.astro';
import BroadcastDiagram from './diagrams/BroadcastDiagram.astro';
import GroupbyDiagram from './diagrams/GroupbyDiagram.astro';
import MeltPivotDiagram from './diagrams/MeltPivotDiagram.astro';
import MergeDiagram from './diagrams/MergeDiagram.astro';
import StackUnstackDiagram from './diagrams/StackUnstackDiagram.astro';

export const referenceComponents = {
  Example,
  Params,
  Pitfall,
  Setup,
  Syntax,
  VersionNote,
  AxisDiagram,
  BroadcastDiagram,
  GroupbyDiagram,
  MeltPivotDiagram,
  MergeDiagram,
  StackUnstackDiagram,
};
