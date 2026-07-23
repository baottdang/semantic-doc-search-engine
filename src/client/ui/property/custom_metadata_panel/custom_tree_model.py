from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt

class TreeItem():
    def __init__(self, data, parent=None):
        self.data = data       
        self.parent = parent      
        self.children = []      
        
        value = data[1]

        # If value is a list of items
        if isinstance(value, list):
            for idx, value in enumerate(value):
                self.children.append(TreeItem([idx, value], self))
        # If value is a dict
        elif isinstance(value, dict):
            for tag, value in value.items():
                self.children.append(TreeItem([tag, value], self))

    def child(self, row):
        return self.children[row]

    def child_count(self):
        return len(self.children)

    def column_count(self):
        return len(self.data) # Should be 2 for key-value pairs

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0

class CustomTreeModel(QAbstractItemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)
        self.rootItem = root

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self.rootItem.child_count()
        return parent.internalPointer().child_count()

    def columnCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self.rootItem.column_count()
        return parent.internalPointer().column_count()

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent

        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role in (Qt.DisplayRole, Qt.EditRole):
            item = index.internalPointer()
            return item.data[index.column()]
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Tag"
            elif section == 1:
                return "Info"
        return None
    
    def set_root(self, rootItem):
        self.beginResetModel()
        self.rootItem = rootItem
        self.endResetModel()

    def flags(self, index):
        if not index.isValid() or (index.column() == 1 and len(index.internalPointer().children) != 0):
            return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        # Model-driven data change
        if role == Qt.EditRole:
            item = index.internalPointer()
            # Update the TreeItem’s value
            item.data[index.column()] = value
            # Emit signal so the view updates
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False
    
    def insertNode(self, row, count, tag, value, parent=QModelIndex()):
        parent_item = self.rootItem if not parent.isValid() else parent.internalPointer()

        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            # Example: add empty key/value
            new_item = TreeItem([tag, value], parent_item)
            parent_item.children.insert(row, new_item)
        self.endInsertRows()
        return True
    
    def insertRows(self, row, count, parent=QModelIndex()):
        # Default override to ensure functionality, DO NOT CALL
        parent_item = self.rootItem if not parent.isValid() else parent.internalPointer()

        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            # Example: add empty key/value
            new_item = TreeItem(["tag", "value"], parent_item)
            parent_item.children.insert(row, new_item)
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        parent_item = self.rootItem if not parent.isValid() else parent.internalPointer()

        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            parent_item.children.pop(row)
        self.endRemoveRows()
        return True


