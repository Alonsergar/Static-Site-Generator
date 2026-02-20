
class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props==None or self.props =="":
            return ""
        props_in_html=""
        for clave,valor in self.props.items():
            props_in_html+=f' {clave}="{valor}"'
        return props_in_html
    def __repr__(self):
        return f"HTMLNode(tag={self.tag},value={self.value},children={self.children},props={self.props})"
  
        
      
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    def to_html(self):
        if self.value==None:
            raise ValueError("Leaf node has no value")
        elif self.tag==None:
            return f"{self.value}"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    def __repr__(self):
        return f"LeafNode(tag={self.tag},value={self.value},props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)
    def to_html(self):
        if self.tag==None :raise ValueError("Parent node needs a tag")
        elif self.children==None: raise ValueError("Parent node needs at least 1 children")
        else:
            children_text=""
            for i in self.children:
                children_text+=i.to_html()
            return f'<{self.tag}{self.props_to_html()}>{children_text}</{self.tag}>'
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
