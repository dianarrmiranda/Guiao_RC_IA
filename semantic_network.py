

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
from collections import Counter


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

class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)


class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,float(e2))

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

        #pds = [d.relation.entity2 for d in self.declarations 
        # if (d.relation.emtity1 == entityB) 
        # and (isinstance(d.relation, (Member, Subtype)))]

        #if entityA in pds:
        #    return True
        
        #return any([self.predecessor(entityA, p) for p in pds])
        return False
    
    def predecessor_path(self, entityA, entityB):

        if entityA == entityB:
            return [entityB]

        for d in self.declarations:
            if isinstance(d.relation, (Subtype, Member)) and d.relation.entity1 == entityB:
                path = self.predecessor_path(entityA, d.relation.entity2)
                if path:
                    return path + [entityB]
                
        return None
    
    def query(self, entity, association=None):
        pds = [self.query(d.relation.entity2, association) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1==entity]
        
        pds_query = [d for sublist in pds for d in sublist]
        q = self.query_local(e1=entity, rel=association)
        lista = []
        for d in q:
            if isinstance(d.relation, Association):
                lista.append(d)
        
        return pds_query + lista
    
    def query2(self, entity, association=None):
        pds = [self.query(d.relation.entity2, association) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1==entity]
        pds_query = [d for sublist in pds for d in sublist]
        self.query_local(e1=entity, rel=association)
        return pds_query + self.query_local(e1=entity, rel=association)

    def query_cancel(self, entity, association):
        pds = [self.query_cancel(d.relation.entity2, association) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1==entity]
        
        q = self.query_local(e1=entity, rel=association)

        pds_query = [d for sublist in pds for d in sublist if d.relation.name not in [l.relation.name for l in q]]
        
        return pds_query + q

    def query_down(self, entity, association, first = True):
        desc = [self.query_down(d.relation.entity1, association, first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2==entity]

        query = [d for sublist in desc for d in sublist]

        if first:
            return query
        
        local = self.query_local(e1 = entity, rel=association)

        return query + local
    
    def query_induce (self, entity, association):
        
        query = self.query_down(entity, association)

        vals = [d.relation.entity2 for d in query]

        count = {}

        for v in vals:
            count[v] = count.get(v, 0) + 1
            
        return max(count, key=count.get)
    
    def query_local_assoc(self, entity, association):
        q = self.query_local(e1=entity, rel=association)

        if all(isinstance(d.relation, AssocOne) for d in q):
            assoc = Counter([d.relation.entity2 for d in q]).most_common(1)
            return (assoc[0][0], assoc[0][1] /len(q))
        if all(isinstance(d.relation, AssocNum) for d in q):
            return sum([d.relation.entity2 for d in q]) / len(q)
        if all(isinstance(d.relation, Association) for d in q):
            val = [d.relation.entity2 for d in q]
            count = [(v, val.count(v)/len(q)) for v in set(val) if val.count(v) > 1 ]
            res = sorted(count, key=lambda x: x[0])
            return sorted(res, key=lambda x: x[1], reverse=True)  
            
 
    def query_assoc_value(self, e, a):
        q = self.query_local(e1=e, rel=a)
        local_values = [d.relation.entity2 for d in q]
        if len(set(local_values)) == 1:
            return local_values[0]
        else:
            max_value = None
            max_score = -1
            for v in set(local_values):
                L = local_values.count(v) / len(local_values)
                H = sum([1 for d in self.query(e, a) if d.relation.entity2 == v]) / len(self.query(e, a))
                score = L + H / 2
                if score > max_score:
                    max_value = v
                    max_score = score
            if max_value is not None:
                return max_value
            else:
                all_values = [d.relation.entity2 for d in self.query(e, a)]
                return max(set(all_values), key=all_values.count)
            
                    


                    



