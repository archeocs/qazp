class Schema(object):
    '''
        Database schema, which includes views (tables and predefined queries)
        and theirs relations.
    '''
    def __init__(self):
        self.views = {} 
        self.rels = {}
        
    def addView(self, view, relation=None):
        '''
            Adds view to schema.
            params:
                - view: view to add
                - relation: optional relation of added view and
                other view already existing in schema. If relation
                is passed and related view does not exist, an exception is raised.
        '''
        if not relation:
            self.views[view] = []
        else:
            rv = relation.related(view).view
            if self.views.has_key(rv):
                self.views[view] = [rv]
                self.views[rv].append(view)
                self.rels[(view, rv)] = relation
                self.rels[(rv, view)] = relation
            else:
                raise Exception('no related views')
                
    def relatedViews(self, view):
        '''
            Finds all views, which have relation with passed one.
        '''
        return self.views[view]
        
    def viewByName(self, name):
        for v in self.views.iterkeys():
            if v.name == name:
                return v
        return None
        
    def attrByName(self, fullName):
        pair = fullName.split('.')
        view = self.viewByName(pair[0])
        if view:
            for attr in view.viewAttrs():
                if attr.realName() == pair[1]:
                    return attr
        return None
        
    def relation(self, view, related):
        '''
            Finds object representing relation between two views.
            If such relation is not fount, method returns None.
            params:
                - view: table or query
                - related: table or query, which is related to view
        '''
        if self.rels.has_key((view, related)):
            return self.rels[(view, related)]
        elif self.rels.has_key((related, view)):
            return self.rels[(related, view)]
        return None
        
    def attributes(self):
        attrs = []
        for v in self.views.iterkeys():
            attrs.extend(v.viewAttrs())
        attrs.sort(cmp=lambda x,y: cmp(x.view.name+'.'+x.realName(), y.view.name+'.'+y.realName()))
        return attrs
        
class ViewAttr(object):
    '''
        Attribute of view. This class is used to define views in database
        schema. It is cloned for each specific query.
    '''
    def __init__(self, name, view, userName=None):
        self.name = name
        self.view = view 
        self.userName = userName
        
    def select(self, visible=True, orderBy=False, groupBy=False, condition=None, aggregate=None, altName=None):
        '''
            Uses parameters and creates attribute used in SELECT clause
            parmas:
                - visible: if true view attribute is visible in SELECt clause.
                - orderBy: if true view attribute is used to order selected rows.
                - groupBy: if true view attribute is used to group aggregated values
                - condition: function used to create conditonal expression in query
                - aggregate: aggregation function
                - altName: alternative (alias) name for attribute
        '''
        sa = SelectAttr(self.name, self.view, self.userName)
        sa.visible = visible
        sa.orderBy = orderBy
        sa.groupBy = groupBy
        sa.condition = condition
        sa.aggregate = aggregate
        sa.altName = altName
        return sa
    
    def _prepareStr(self, alias):
        return '%s.%s' % (alias, self.name)
            
    def toString(self, alias):
        return self._prepareStr(alias)
     
    def realName(self):
        if self.userName:
            return self.userName
        return self.name
        
    def fullName(self):
        return self.view.name+'.'+self.realName()
        
        
class SelectAttr(ViewAttr):
    '''
        Cloned version of view attributed. It represents properties of view attribute
        specific for builded query.
    '''
    def __init__(self, name, view, userName=None):
        ViewAttr.__init__(self, name, view, userName)
        self.visible = True
        self.orderBy = False
        self.groupBy = False
        self.condition = None
        self.aggregate=None
        self.altName = None
    
    def _prepareStr(self, alias):
        base = ViewAttr._prepareStr(self, alias)
        if self.aggregate:
            base = self.aggregate(base)
        if self.altName:
            base += ' as '+self.altName
        return base
    
    def realName(self):
        if self.altName:
            return self.altName
        return ViewAttr.realName(self)
        

class IView(object):

    def __init__(self, name):
        self.name = name
        
    def attribute(self, name):
        '''
           Finds attribute in view by passed name.
           In default implementation this method raise exception
        '''
        raise Exception('Not implemented')
    
    @property    
    def source(self):
        '''
            Source of this view - for example table name, or
            query selecting values from table(s).
            In default implemention this method raise an exception
        '''
        raise Exception('Not implemented')
        
    def viewAttrs(self):
        raise Exception('Not implemented')
        
    def __getitem__(self, key):
        return self.attribute(key)
        
class View(IView):
    '''
        Represents table in database or predefined query,
        which might be used as subquery.
    '''
    
    def __init__(self, src, name, attrNames):
        '''
            Initialise new view. 
            params:
                - src: definition of view (table name, select query) used to build query.
                - name: humand friendly name of view.
                - attrNames: names of attributes.
        '''
        IView.__init__(self, name)
        self._src = src
        self.attrs = {}
        for n in attrNames:
            self.attrs[n] = ViewAttr(n, self)
    
    def attribute(self, name):
        '''
            Finds attribute in view by passed name.
        '''
        return self.attrs[name]
    
    @property
    def source(self):
        return self._src
        
    def viewAttrs(self):
        return self.attrs.itervalues()

class Condition(object):
    '''
        Condition(s) for single attribute instance.
        If one attribute has more than one condition,
        they are all chainde in one object.
    '''
    def __init__(self, logFunc, operator):
        '''
            Initailise constructor. Each instance might have
            childrens - other conditions assigned to the same
            attribute instance. 
            It is suggested to use ConditionChain class to build
            complex conditions.
            params:
                - logFunc - OR or AND, NOT AND, etc.
                - operator - =, <, >=, ...
        '''
        self.logFunc = logFunc
        self.operator = operator
        self.next = None # next condition in chain
        
    def toString(self, attribute, index=0):
        '''
            Creates string used in query. 
        '''
        base = ''
        if index > 0:
            base += self.logFunc
        base += (' %s %s :param%d ' % (attribute, self.operator, index))
        idx = index + 1
        if self.next:
            nc = self.next.toString(attribute, idx)
            base += ' '+nc[0]
            return (base, nc[1])
        else:
            return (base, idx)
            
    def paramNames(self, index):
        arr = []
        arr.append('param%d'%index)
        idx = index + 1
        nx = self.next
        while nx:
            arr.append('param%d'%idx)
            nx = nx.next
            idx += 1
        return (arr, idx)

def orCondition(operator):
    return Condition('OR', operator)

def andCondition(operator):
    return Condition('AND', operator)
    
class ConditionChain(object):
    '''
        Conditions for attribute.
    '''
    def __init__(self):
        self.cond = None
    
    def addOr(self, operator):
        '''
            Adds alternative condition to the chain.
        '''
        return self.add(orCondition(operator))
        
    def addAnd(self, operator):
        '''
            Adds conjunction condition to the chain.
        '''
        return self.add(andCondition(operator))
        
    def add(self, condition):
        '''
            Adds condition to the chain. 
        '''
        if not self.cond:
            self.cond = condition
        else:
            nx = self.cond
            while nx.next:
                nx = nx.next
            nx.next = condition
        return self
        
    def build(self):
        return self.cond
        
class Relation(object):
    '''
        Representation of relation between two views. Each relations contains
        one or more pairs of attributes.
    '''
    def __init__(self, pairs):
        '''
            Initialise relation with pairs of attributes.
        '''
        self.pairs = pairs
        
    def related(self, view):
        '''
            Finds related view.
        '''
        return self.pairs[0].related(view)
        
    def toString(self, vleft, vright):
        '''
            Creates string representation of relation used in JOIN part of query.
        '''
        return ' AND '.join([p.toString(vleft, vright) for p in self.pairs])
        
class AttrPair(object):

    '''
        Pair of attributes which defines part of relation of 
        two views.
    '''
    def __init__(self, leftAttr, rightAttr):
        '''
            Initialize new pair of attributes.
            params:
                - leftAttr: attribute from first view.
                - rightAttr: attribute from view related to first one.
        '''
        self.left = leftAttr
        self.right = rightAttr
        
    def related(self, view):
        '''
            Finds view related to passed one. Choice is based on
            attributes in this pair.
        '''
        if self.left.view == view:
            return self.right
        elif self.right.view == view:
            return self.left
        else:
            return None
    
    def attribute(self, view):
        '''
            Finds matching attribute from view related to passed one.
            If pairs does not define relation for view, exception is raised.
        '''
        if view == self.left.view:
            return self.left
        elif view == self.right.view:
            return self.right
        else:
            raise Exception('Views do not match')
            
    def toString(self, vleft, vright):
        '''
            Creates string representation of pair used in JOIN part of query.
        '''
        a = vleft.alias+'.'+self.attribute(vleft.view).name
        b = vright.alias+'.'+self.attribute(vright.view).name
        return a+' = '+b
