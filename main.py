from DENetwork.Network import *

N = Network()
#N.create_network("3;-2;1;-1;2;0;-1","w100;w100;w100;w100;w100;w100;x100;w100;w100;w100")
#N.define_collision_domains([[12,13]])
#N.generate_paths()
#N.generate_frames(10,0.0,per_locally=1)
#N.add_frame_params([5,10],[0.5,0.5],[0.8,0.5], [1000, 1400])
#N.generate_xml_output('prueba')
#network_description, link_description = N.get_network_description_from_xml('mac_sim_params.xml')
#collision_domain = N.get_collision_domains_xml('mac_sim_params.xml')
#number_frames, percentages = N.get_frames_description_from_xml('mac_sim_params.xml')
#period, per_periods, deadlines, sizes = N.get_frames_variables_from_xml('mac_sim_params.xml')
N.create_network_from_xml('mac_sim_params.xml', 'prueba.xml')
