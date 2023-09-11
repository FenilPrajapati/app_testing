import { KanbanController } from 'web/static/src/views/kanban/kanban_controller';

export class CustomKanbanController extends KanbanController {
    setup() {
        super.setup();

        // Modify the CSS class for KanbanRecord
        const kanbanRenderer = this.getComponent('KanbanRenderer');
        kanbanRenderer.kanbanRecordClass = 'o_kanban_record_full_width';

        // Update KanbanRecord width using CSS
        const styleElement = document.createElement('style');
        styleElement.textContent = `
            .o_kanban_record_full_width .o_kanban_record {
                width: 100%;
            }
        `;
        this.env.qweb.addCSS(styleElement);
    }
}
