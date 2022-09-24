from json import load
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

from robject import RObject, Rest, load_robject, RObject_Type
from preferences import PREFERENCES


class RObjectManager:
    def __init__(self):
        self.tree_widget: QTreeWidget = None

    @property
    def selected_robject(self) -> RObject:
        if self.tree_widget is None:
            return None
        tree_widget_item = self.tree_widget.currentItem()
        if tree_widget_item is None or tree_widget_item.childCount() != 0:
            return None
        return load_robject(tree_widget_item.text(0), tree_widget_item.parent().text(0))

    def set_tree_widget(self, tree_widget: QTreeWidget):
        self.tree_widget = tree_widget

    def populate_tree(self, show: RObject_Type = RObject_Type.ANY):
        self.tree_widget.clear()
        for category_path in PREFERENCES.robject_directory.iterdir():
            if category_path.is_dir():
                category = category_path.name
                # Validate path
                if not all([category.startswith("["), category.endswith("]")]):
                    continue
                tree_category = QTreeWidgetItem([category])
                if any([
                    show == RObject_Type.RHYTHM and category != "[]",
                    show == RObject_Type.REST and category == "[]",
                    show == RObject_Type.ANY
                ]):
                    robjects = []
                    for id in [robject_path.stem for robject_path in category_path.iterdir()]:
                        robjects.append(QTreeWidgetItem(load_robject(id, category).list))
                    tree_category.addChildren(robjects)
                self.tree_widget.addTopLevelItem(tree_category)
                self.tree_widget.resizeColumnToContents(0)
