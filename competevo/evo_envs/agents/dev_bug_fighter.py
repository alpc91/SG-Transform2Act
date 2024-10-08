from gym_compete.new_envs.agents import *
from gymnasium.spaces import Box
import numpy as np
import os

from lxml.etree import XMLParser, parse, ElementTree, Element, SubElement
from lxml import etree
from io import BytesIO
from lib.utils import get_single_body_qposaddr,get_graph_fc_edges
from competevo.evo_envs.robot.xml_robot import Robot

SCALE_MAX = 0.3

class DevBugFighter(BugFighter):
    CFRC_CLIP = 100.

    COST_COEFS = {
        'ctrl': 1e-1,
        # 'pain': 1e-4,
        # 'attack': 1e-1,
    }

    JNT_NPOS = {
        0: 7,
        1: 4,
        2: 1,
        3: 1,
    }

    def __init__(self, agent_id, cfg, xml_path=None, n_agents=2):
        if xml_path is None:
            xml_path = os.path.join(os.path.dirname(__file__), "assets", "bug_body.xml")
        super(DevBugFighter, self).__init__(agent_id, xml_path, n_agents)

        parser = XMLParser(remove_blank_text=True)
        self.tree = parse(xml_path, parser=parser)
        self.cur_xml_str = etree.tostring(self.tree, pretty_print=True).decode('utf-8')

        self.cfg = cfg


        self.robot = Robot(cfg.robot_cfg, xml=xml_path)

        self.stage = "attribute_transform"
        self.scale_vector = np.random.uniform(low=-1., high=1., size=30)
    
    @property
    def flag(self):
        return "dev"

    def set_env(self, env):
        super(BugFighter, self).set_env(env)
        self.arena_id = self.env.geom_names.index('arena')
        self.arena_height = self.env.model.geom_size[self.arena_id][1] * 2

        # dimension definition
        self.scale_state_dim = self.scale_vector.size
        self.sim_obs_dim = self.observation_space.shape[0]
        self.sim_action_dim = self.action_space.shape[0]
        self.stage_state_dim = 1
        
        self.action_dim = self.sim_action_dim + self.scale_state_dim
        self.state_dim = self.stage_state_dim + self.scale_state_dim + self.sim_obs_dim

        # print(self.state_dim, self.action_dim)
            
    def set_design_params(self, action):
        scale_state = action[:self.scale_state_dim]
        self.scale_vector = scale_state
        # print(scale_state)

        design_params = self.scale_vector * SCALE_MAX
        a = design_params + 1.
        b = design_params*0.5 + 1 # for gear only

        def multiply_str(s, m):
            res = [str(float(x) * m) for x in s.split()]
            res_str = ' '.join(res)
            return res_str

        agent_body = self.tree.find('body')
        for body in agent_body.iter('body'):
            cur_name = body.get('name')

            # 1
            if cur_name == "1":
                geom = body.find('geom') #1
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[0])
                    geom.set("fromto", p)

            if cur_name == "11":
                p = body.get("pos")
                p = multiply_str(p, a[0])
                body.set("pos", p)

                geom = body.find('geom') #11
                p = geom.get("size")
                p = multiply_str(p, a[1])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[2])
                    geom.set("fromto", p)

            if cur_name == "111":
                p = body.get("pos")
                p = multiply_str(p, a[2])
                body.set("pos", p)

                geom = body.find('geom') #111
                p = geom.get("size")
                p = multiply_str(p, a[3])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[4])
                    geom.set("fromto", p)

            # 2
            if cur_name == "2":
                geom = body.find('geom') #2
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[5])
                    geom.set("fromto", p)

            if cur_name == "12":
                p = body.get("pos")
                p = multiply_str(p, a[5])
                body.set("pos", p)

                geom = body.find('geom') #12
                p = geom.get("size")
                p = multiply_str(p, a[6])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[7])
                    geom.set("fromto", p)

            if cur_name == "112":
                p = body.get("pos")
                p = multiply_str(p, a[7])
                body.set("pos", p)

                geom = body.find('geom') #112
                p = geom.get("size")
                p = multiply_str(p, a[8])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[9])
                    geom.set("fromto", p)

            # 3
            if cur_name == "3":
                geom = body.find('geom') #3
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[10])
                    geom.set("fromto", p)

            if cur_name == "13":
                p = body.get("pos")
                p = multiply_str(p, a[10])
                body.set("pos", p)

                geom = body.find('geom') #13
                p = geom.get("size")
                p = multiply_str(p, a[11])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[12])
                    geom.set("fromto", p)

            if cur_name == "113":
                p = body.get("pos")
                p = multiply_str(p, a[12])
                body.set("pos", p)

                geom = body.find('geom') #113
                p = geom.get("size")
                p = multiply_str(p, a[13])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[14])
                    geom.set("fromto", p)

            # 4
            if cur_name == "4":
                geom = body.find('geom') #4
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[15])
                    geom.set("fromto", p)

            if cur_name == "14":
                p = body.get("pos")
                p = multiply_str(p, a[15])
                body.set("pos", p)

                geom = body.find('geom') #14
                p = geom.get("size")
                p = multiply_str(p, a[16])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[17])
                    geom.set("fromto", p)

            if cur_name == "114":
                p = body.get("pos")
                p = multiply_str(p, a[17])
                body.set("pos", p)

                geom = body.find('geom') #114
                p = geom.get("size")
                p = multiply_str(p, a[18])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[19])
                    geom.set("fromto", p)

            # 5
            if cur_name == "5":
                geom = body.find('geom') #5
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[20])
                    geom.set("fromto", p)

            if cur_name == "15":
                p = body.get("pos")
                p = multiply_str(p, a[20])
                body.set("pos", p)

                geom = body.find('geom') #15
                p = geom.get("size")
                p = multiply_str(p, a[21])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[22])
                    geom.set("fromto", p)

            if cur_name == "115":
                p = body.get("pos")
                p = multiply_str(p, a[22])
                body.set("pos", p)

                geom = body.find('geom') #115
                p = geom.get("size")
                p = multiply_str(p, a[23])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[24])
                    geom.set("fromto", p)
            
            # 6
            if cur_name == "6":
                geom = body.find('geom') #6
                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[25])
                    geom.set("fromto", p)

            if cur_name == "16":
                p = body.get("pos")
                p = multiply_str(p, a[25])
                body.set("pos", p)

                geom = body.find('geom') #16
                p = geom.get("size")
                p = multiply_str(p, a[26])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[27])
                    geom.set("fromto", p)

            if cur_name == "116":
                p = body.get("pos")
                p = multiply_str(p, a[27])
                body.set("pos", p)

                geom = body.find('geom') #116
                p = geom.get("size")
                p = multiply_str(p, a[28])
                geom.set("size", p)

                if geom is not None:
                    p = geom.get("fromto")
                    p = multiply_str(p, a[29])
                    geom.set("fromto", p)

        agent_actuator = self.tree.find('actuator')
        for motor in agent_actuator.iter("motor"):
            cur_name = motor.get("name").split('_')[0]

            if cur_name == "11":
                p = motor.get("gear")
                p = multiply_str(p, b[1])
                motor.set("gear", p)

            if cur_name == "111":
                p = motor.get("gear")
                p = multiply_str(p, b[3])
                motor.set("gear", p)

            if cur_name == "12":
                p = motor.get("gear")
                p = multiply_str(p, b[6])
                motor.set("gear", p)

            if cur_name == "112":
                p = motor.get("gear")
                p = multiply_str(p, b[8])
                motor.set("gear", p)

            if cur_name == "13":
                p = motor.get("gear")
                p = multiply_str(p, b[11])
                motor.set("gear", p)

            if cur_name == "113":
                p = motor.get("gear")
                p = multiply_str(p, b[13])
                motor.set("gear", p)

            if cur_name == "14":
                p = motor.get("gear")
                p = multiply_str(p, b[16])
                motor.set("gear", p)

            if cur_name == "114":
                p = motor.get("gear")
                p = multiply_str(p, b[18])
                motor.set("gear", p)
            
            if cur_name == "15":
                p = motor.get("gear")
                p = multiply_str(p, b[21])
                motor.set("gear", p)

            if cur_name == "115":
                p = motor.get("gear")
                p = multiply_str(p, b[23])
                motor.set("gear", p)

            if cur_name == "16":
                p = motor.get("gear")
                p = multiply_str(p, b[26])
                motor.set("gear", p)

            if cur_name == "116":
                p = motor.get("gear")
                p = multiply_str(p, b[28])
                motor.set("gear", p)

        # print(etree.tostring(self.tree, pretty_print=True).decode('utf-8'))
        self.cur_xml_str = etree.tostring(self.tree, pretty_print=True).decode('utf-8')
        # print(self.cur_xml_str)


    def before_step(self):
        self.posbefore = self.get_qpos()[:2].copy()
    
    def after_step(self, action):
        """ RoboSumo design.
        """
        self.posafter = self.get_qpos()[:2].copy()
        # Control cost
        control_reward = - self.COST_COEFS['ctrl'] * np.square(action).sum()

        alive_reward = 2.0

        return control_reward, alive_reward

    def if_use_transform_action(self):
        return ['attribute_transform', 'execution'].index(self.stage)

    def _get_obs(self, stage=None):
        '''
        Return agent's observations
        '''
        # update stage tag from env
        if stage not in ['attribute_transform', 'execution']:
            stage = 'attribute_transform'
        self.stage = stage

        # Observe self
        self_forces = np.abs(np.clip(
            self.get_cfrc_ext(), -self.CFRC_CLIP, self.CFRC_CLIP))
        # obs  = [
        #     self.get_qpos().flat,           # self all positions
        #     self.get_qvel().flat,           # self all velocities
        #     self_forces.flat,               # self all forces
        # ]

        # self_forces_id = np.array([[0,0,0],[0,1,2],[1,2,3],[0,4,5],[4,5,6],[0,7,8],[7,8,9],[0,10,11],[10,11,12],[0,13,14],[13,14,15],[0,16,17],[16,17,18]])


        # Observe opponents
        other_qpos = self.get_other_qpos()
        # if other_qpos.shape == (0,):
        #     # other_qpos = np.zeros(2) # x and y
        #     other_qpos = np.random.uniform(-5, 5, 2)

        # obs.extend([
        #     other_qpos[:2].flat,    # opponent torso position
        # ])

        # torso_xmat = self.get_torso_xmat()
        # # print(torso_xmat)
        # obs.extend([
        #     torso_xmat.flat,
        # ])
        qpos = self.get_qpos()
        qvel = self.get_qvel()
        # root_pos = qpos[:2]
        # root_pos = np.append(root_pos, 0)
        root_pos = np.array([0,0,0])
        obs = []
        idx = 0
        agent_body = self.tree.find('body')
        for body in agent_body.iter('body'):
            cur_name = body.get('name')
            # forces = [self_forces[id] for id in self_forces_id[idx]]
            if cur_name == "0":
                obs_i = [self.env.data.body(self.scope + "/" +cur_name).xipos - root_pos, other_qpos, np.array([0,0,9.8]),  self_forces[idx], qvel[:6],self.env.data.body(self.scope + "/" +cur_name).xipos[2:3],np.zeros(2)]
            else:
                qs, qe = get_single_body_qposaddr(self.env.model, self.scope + "/" + cur_name)
                if qe - qs >= 1:
                    assert qe - qs == 1
                    angle =  np.append(self.env.data.qpos[qs:qe], self.env.data.qvel[qs-1-self.id:qe-1-self.id])
                else:
                    angle = np.zeros(2)
                obs_i = [self.env.data.body(self.scope + "/" +cur_name).xipos - root_pos, other_qpos,  np.array([0,0,9.8]),  self_forces[idx], np.zeros(6),self.env.data.body(self.scope + "/" +cur_name).xipos[2:3],angle]


            obs_i = np.concatenate(obs_i)
            obs.append(obs_i)
            idx += 1


        num_nodes = np.array([len(obs)])
        sim_obs = np.concatenate(obs)
        assert np.isfinite(sim_obs).all(), "Ant observation is not finite!!"

        edges = self.robot.get_gnn_edges()
        # edges = get_graph_fc_edges(num_nodes[0])

        obs = [np.array([self.if_use_transform_action()]), self.scale_vector, edges, num_nodes, sim_obs]
        return obs

    def get_torso_xmat(self):
        return self.env.data.xmat[self.body_ids[self.body_names.index('agent%d/0' % self.id)]]

    def set_observation_space(self):
        obs = self._get_obs(self.stage)[-1]
        self.obs_dim = obs.size
        high = np.inf * np.ones(self.obs_dim)
        low = -high
        self.observation_space = Box(low, high)

    def reset_agent(self,**kwargs):
        xpos = self.get_qpos()[0]
        if xpos * self.GOAL > 0:
            self.set_goal(-self.GOAL)
        if xpos > 0:
            self.move_left = True
        else:
            self.move_left = False
        
        self.stage = 'attribute_transform'
        self.scale_vector = np.random.uniform(low=-1., high=1., size=30)