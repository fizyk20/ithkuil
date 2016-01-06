from arpeggio import PTNodeVisitor

def pass_visitor(num=0):
    def visitor(a, node, children):
        print("Passing: ", children[num])
        return children[num]
    return visitor

def collect_visitor(a, node, children):
    return ''.join(children)

def constant_visitor(const):
    def visitor(a, node, children):
        return const
    return visitor

def constant_add_visitor(const, num=0):
    def visitor(a, node, children):
        children[num].update(const)
        return children[num]
    return visitor
    
def dict_visitor(key):
    def visitor(a, node, children):
        return { key: ''.join(children) }
    return visitor

def dict_combine_visitor(a, node, children):
    print("Combining: ", children)
    result = {}
    for child in children:
        if isinstance(child, dict): result.update(child)
    return result

def dict_append_visitor(to_append):
    def visitor(a, node, children):
        result = dict_combine_visitor(a, node, children)
        result.update(to_append)
        return result
    return visitor

class IthkuilVisitor(PTNodeVisitor):

    visit_consonant = pass_visitor()

    visit_vowel = pass_visitor()

    visit_consonants = collect_visitor

    visit_vowels = collect_visitor
    
    visit_formative = dict_append_visitor({ 'type': 'formative' })

    visit_stress_formative = pass_visitor()

    visit_penultimate_stress_formative = constant_add_visitor({ 'stress': -2 })

    visit_ultimate_stress_formative = constant_add_visitor({ 'stress': -1 })

    visit_antepenultimate_stress_formative = constant_add_visitor({ 'stress': -3 })

    visit_preantepenultimate_stress_formative = constant_add_visitor({ 'stress': -4 })

    visit_main_formative = dict_combine_visitor

    visit_prefix = dict_combine_visitor

    visit_prefix_no_cv_vl = dict_combine_visitor

    visit_vr = dict_visitor('Vr')

    visit_cg = dict_visitor('Cg')

    def visit_cs(self, node, children):
        children.insert(1, '-')
        return dict_visitor('Cs')(self, node, children)

    visit_vl = dict_visitor('Vl')

    visit_cv = dict_visitor('Cv')

    visit_root_part_we = dict_combine_visitor

    visit_root_part = dict_combine_visitor

    visit_vc = dict_visitor('Vc')

    visit_civi = dict_visitor('Ci+Vi')

    visit_ca = dict_visitor('Ca')

    visit_has_format = dict_combine_visitor

    visit_root = dict_visitor('Cr')

    def visit_incorporated_root(self, node, children): return { 'Cx': children[0]['Cr'], 'Vp': children[1] }

    visit_vf_no_format = dict_visitor('Vf')

    visit_vf = dict_visitor('Vf')

    visit_vf_format = pass_visitor()
    
    visit_suffix_fe_type = pass_visitor()

    def visit_suffix_format_exp(self, node, children): return { 'type': children[1], 'degree': children[0] }

    def visit_suffix(self, node, children): return { 'type': children[1], 'degree': children[0] }
    
    def visit_suffixes(self, node, children): return { 'VxC': children }

    def visit_suffixes_fe(self, node, children): return { 'VxC': children }

    def visit_stop(self, node, children): return '’'

    visit_geminable = pass_visitor()

    visit_consonant4 = pass_visitor()

    visit_tone = dict_visitor('tone')
    
    visit_cb = dict_visitor('Cb')

    visit_bias = pass_visitor(1)

    visit_validation = pass_visitor()
    
    # vebal adjuncts
    
    visit_verbal_adjunct = dict_append_visitor({ 'type': 'verbal adjunct' })
    
    visit_cl = dict_visitor('Cl')
    
    visit_vs = dict_visitor('Vs')
    
    visit_ve = dict_visitor('Ve')
    
    visit_vm = dict_visitor('Vm')

    visit_word = pass_visitor()
    
    # personal adjuncts
    
    visit_personal_adjunct = dict_append_visitor({ 'type': 'personal adjunct' })
    
    visit_single_referent = dict_combine_visitor
    
    visit_short_form = dict_combine_visitor
    
    visit_long_form = dict_combine_visitor
    
    visit_c1 = dict_visitor('C1')
    
    visit_vcp = collect_visitor
    
    visit_vcp1 = dict_visitor('Vc')
    
    visit_vcp2 = dict_visitor('Vc2')
    
    visit_cz = dict_visitor('Cz')
    
    visit_vz = dict_visitor('Vz')
    
    visit_csp = collect_visitor
    
    visit_vsp = collect_visitor
    
    def visit_rev_suffix(self, node, children):
        return { 'type': children[0], 'degree': children[1] }
    
    def visit_rev_suffixes(self, node, children):
        return { 'VxC': children }
    
    visit_conjunct_form = dict_combine_visitor
    
    visit_collapsed_form = dict_combine_visitor
    
    visit_high_tone = dict_visitor('tone')
    
    visit_four_tone = dict_visitor('tone')
    
    visit_dual_referent = dict_combine_visitor
    
    visit_vw = dict_visitor('Vw')
    
    visit_ck = dict_visitor('Ck')
    
    visit_c2 = dict_visitor('C2')
    
    def visit_aspectual_adjunct(self, node, children):
        return { 'type': 'aspectual adjunct', 'Vs': ''.join(children) }
    
    def visit_affixual_adjunct(self, node, children):
        return { 'type': 'affixual adjunct', 'VxC': { 'type': children[1], 'degree': ''.join(children[:-1]) } }
    
    visit_bias_adjunct = dict_append_visitor({ 'type': 'bias adjunct' })
