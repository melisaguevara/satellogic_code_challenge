from .models import Task


class TasksService:
    def __init__(self):
        self.db_model = Task
        self.LONGEST_SET_TO_PROCESS_IN_EXPONENTIAL_TIME = 35

    def get_next_batch_of_executable_tasks(self, new_tasks):
        self.db_model.save_tasks(new_tasks)
        in_queue_tasks = self.db_model.get_tasks_by_status('IN_QUEUE')
        tasks_to_execute_next = self.get_most_profitable_subset_of_tasks(
            in_queue_tasks)
        self._update_tasks_status(tasks_to_execute_next, 'PROCESSING')
        return tasks_to_execute_next.__dict__

    def get_most_profitable_subset_of_tasks(self, tasks):
        # We separate tasks with no resources as they are always compatible with other tasks
        # As so, they can always be merged with a profitable subset
        tasks_set_with_no_resources, tasks_set_with_resources = self._get_subsets_of_tasks_by_resource_usage(
            tasks)

        if (len(tasks_set_with_resources.tasks) < self.LONGEST_SET_TO_PROCESS_IN_EXPONENTIAL_TIME):
            profitable_subset = self.find_most_profitable_subset_among_all_compatible_subsets(
                tasks_set_with_resources.tasks)
        else:
            profitable_subset = self.find_most_profitable_subset_among_some_compatible_subsets(
                tasks_set_with_resources.tasks)

        profitable_subset.merge_subsets(
            tasks_set_with_no_resources)

        return profitable_subset

    def find_most_profitable_subset_among_all_compatible_subsets(self, input_tasks_list):
        ''' This method creates all the possible subsets of compatible tasks
            It tracks the max profit to return the most profitable subset
            This runs in exponential time, it should be used only with small inputs '''

        initial_empty_subset = TasksSubset()
        subsets = [initial_empty_subset]
        most_profitable_subset = initial_empty_subset

        for task in input_tasks_list:
            new_subsets = []
            for tasks_subset in subsets:
                if tasks_subset.do_not_conflict_with(task['resources']):
                    # Create a NEW subset with the previous elements + the new task
                    new_subset = TasksSubset(tasks_subset)
                    new_subset.add_task(task)
                    if new_subset.total_profit > most_profitable_subset.total_profit:
                        most_profitable_subset = new_subset
                    new_subsets.append(
                        new_subset)

            subsets.extend(new_subsets)

        return most_profitable_subset

    def find_most_profitable_subset_among_some_compatible_subsets(self, tasks):
        ''' This method creates some of the possible subsets of compatible tasks
            It tracks the max profit to return the most profitable subset found
            This runs in quadratic time, it can be used with large inputs '''

        most_profitable_subset = TasksSubset()

        sorted_tasks = self._sort_tasks_by_profit(tasks)
        for outter_task in sorted_tasks:
            compatible_tasks = TasksSubset()
            compatible_tasks.add_task(outter_task)
            for inner_task in sorted_tasks:
                if inner_task != outter_task:
                    if compatible_tasks.do_not_conflict_with(inner_task['resources']):
                        compatible_tasks.add_task(inner_task)
            if compatible_tasks.total_profit > most_profitable_subset.total_profit:
                most_profitable_subset = compatible_tasks

        return most_profitable_subset

    def _get_subsets_of_tasks_by_resource_usage(self, tasks):
        tasks_using_no_resources = TasksSubset()
        tasks_using_resources = TasksSubset()
        for task in tasks:
            if len(task['resources']) == 0:
                tasks_using_no_resources.add_task(task)
            else:
                tasks_using_resources.add_task(task)
        return tasks_using_no_resources, tasks_using_resources

    def _sort_tasks_by_profit(self, tasks):
        # Tasks with equal profit will be sorted based on resource usage, favoring tasks using fewer resources.
        return sorted(tasks, key=lambda task: (task['profit'], -len(task['resources'])), reverse=True)

    def _update_tasks_status(self, tasks_to_update, new_status):
        tasks_ids = [
            task['id']
            for task in tasks_to_update.tasks
        ]
        self.db_model.update_tasks_status(tasks_ids, new_status)


class TasksSubset:
    def __init__(self, tasks_subset={}) -> None:
        self.tasks = list(getattr(tasks_subset, 'tasks', []))
        self.resources = set(getattr(tasks_subset, 'resources', set()))
        self.total_profit = getattr(tasks_subset, 'total_profit', 0)

    def do_not_conflict_with(self, required_resources):
        resources_intersection = self.resources.intersection(
            set(required_resources))
        return len(resources_intersection) == 0

    def add_task(self, new_task):
        self.tasks.append(new_task)
        self.resources.update(new_task['resources'])
        self.total_profit += new_task['profit']

    def merge_subsets(self, new_subset):
        self.tasks = self.tasks + new_subset.tasks
        self.resources = self.resources.union(new_subset.resources)
        self.total_profit = self.total_profit + new_subset.total_profit
