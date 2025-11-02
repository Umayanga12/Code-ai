class PhaseAwareExecutor(AgentExecutor):
    def _take_next_step_(self, *arg,**kwargs):
        name_to_tool_map, start_time, llm_prefix, agent_scratchpad = args[:4]

        phase = self.memory.chat_memory.messages[-1].addtional_kwargs.get('phase','gathering') if self.memory.chat_memory.messages else 'gathering'

        self.agent.llm_chain.prompt = self.agent.llm_chain.prompt.partial(phase=phase)

        next_step_output = super()._take_next_step_(*arg,**kwargs)
