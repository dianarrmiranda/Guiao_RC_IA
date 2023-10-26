

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#
class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    
    def list_associations(self):
        associations = set([])
        for d in self.query_local():
            if isinstance(d.relation, Association):
                associations.add(d.relation.name)
        return associations

    def list_objects(self):
        objects = set([])
        for d in self.query_local():
            if isinstance(d.relation, Member):
                objects.add(d.relation.entity1)
        return objects
    
    def list_users(self):
        users = set([])
        for d in self.query_local():
            users.add(d.user)
        return users
    
    def list_types(self):
        types = set([])
        for d in self.query_local():
            if isinstance(d.relation, (Subtype, Member)):
                types.add(d.relation.entity2)
        return types
    
    def list_local_associations(self, entity):
        associations = set([])
        for d in self.query_local(None, entity):
            if isinstance(d.relation, Association):
                associations.add(d.relation.name)
        return associations
    
    def list_relations_by_user(self, user):
        relations = set([])
        for d in self.query_local(user):
            relations.add(d.relation.name)
        return relations
    
    def associations_by_user(self, user):
        associations = set([])
        for d in self.query_local(user):
            if isinstance(d.relation, Association):
                associations.add(d.relation.name)
        return len(associations)
    
    def list_local_associations_by_entity(self, entity):
        assocByEnt = []
        for d in self.query_local(None, entity):
            if isinstance(d.relation, Association):
                if (d.relation.name, d.user) not in assocByEnt:
                    assocByEnt.append((d.relation.name, d.user))
        return assocByEnt
    
    def predecessor(self, entityA, entityB):
        queue = ([entityB])
        visited = set([entityB])

        while queue:
            current_entity = queue.pop()
            if current_entity == entityA:
                return True
            for d in self.query_local(None, current_entity, None, None):
                if isinstance(d.relation, (Subtype, Member)):
                    predecessor = d.relation.entity2
                    if predecessor not in visited:
                        queue.append(predecessor)
                        visited.add(predecessor)
        return False
    

    




