import time, gc
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn , BarColumn, TimeRemainingColumn,TaskProgressColumn
from rich.console import Console

console = Console()

class Unit:
    def __init__(self, name, mCost, gCost, population, hp, shield, arm, mana, training_time, utype):
        self.name = name
        self.mCost = mCost
        self.gCost = gCost
        self.population = population
        self.hp = hp
        self.shield = shield
        self.arm = arm
        self.mana = mana
        self.training_time = training_time
        self.utype = utype

    def spawn(self):
        print(f'{self.name}이/가 워프되었습니다.')

    def death(self):
        self.hp = 0
        print(f'{self.name}이/가 사망했습니다...')
        unit_manager.remove(self)  # 묘지로 이동

class AttackUnit(Unit):
    def __init__(self, name:str, mCost:int, gCost:int, population:int, hp:int, dmg:int, shield:int, arm:int, mana:list, training_time:int, attackAble:list, utype:int):
        super().__init__(name, mCost, gCost, population, hp, shield, arm, mana, training_time, utype)
        self.dmg = dmg
        self.attackAble = attackAble

    def attack(self, target: Unit):
        if self.attackAble[target.utype]:
            if target.hp - self.dmg <= 0:
                console.print(f"[bold red]{target.name}을/를 처치했습니다!")
            else:
                target.hp -= self.dmg
                print(f'{self.name}이/가 {target.name}에게 {self.dmg} 피해를 입힘.\n상대 체력 : {target.hp}')
        else:
            print(f'{target.name}을 공격할 수 없습니다!')

class MagicUnit(Unit):
    def __init__(self):
        pass
    
class research:
    def __init__(self, name, mCost, gCost, research_time, research_TF):
        self.name = name
        self.mCost = mCost
        self.gCost = gCost
        self.research_time = research_time
        self.research_TF = research_TF

class Building:
    def __init__(self, name, mCost, gCost, build_time):
        self.name = name
        self.mCost = mCost
        self.gCost = gCost
        self.build_time = build_time

class TrainingBuilding(Building):
    def __init__(self, name, mCost, gCost, build_time):
        super().__init__(name, mCost, gCost, build_time)
        
    def training(self, unit:Unit):
        console.print(f"[yellow][{self.name}][/yellow]에서 [bold blue]{unit.name}[/bold blue]을(를) 훈련합니다")
        with Progress(f"훈련중...", BarColumn(), TaskProgressColumn(), SpinnerColumn(), TimeElapsedColumn()) as progress:
            task = progress.add_task(f"[cyan]{unit.name} 훈련 중...", total=unit.training_time)
            while not progress.finished:
                time.sleep(0.1)
                progress.update(task, advance=0.1)
        console.print(f"[green]{unit.name} 훈련 완료!")
        return unit_manager.allyRegister(unit)

class ResearchBuilding(Building):
    def __init__(self, name, mCost, gCost, build_time):
        super().__init__(name, mCost, gCost, build_time)
    
    def research(self, research:research):
        console.print(f"[yellow][{self.name}][/yellow]에서 [bold blue]{research.name}[/bold blue]을(를) 연구합니다")
        with Progress(f"연구중...", BarColumn(), TaskProgressColumn(), SpinnerColumn(), TimeElapsedColumn()) as progress:
            task = progress.add_task(f"[cyan]{research.name} 연구 중...", total=research.research_time)
            while not progress.finished:
                time.sleep(0.1)
                progress.update(task, advance=0.1)
        console.print(f"[green]{research.name} 연구 완료!")
        return research.research_TF == True
        
# =====================
#      유닛매니저
# =====================

class UnitManager:
    def __init__(self):
        self.active_units = []
        self.dead_units = []
        self.ally_units = []

    def register(self, unit):
        self.active_units.append(unit)

    def allyRegister(self, unit):
        self.ally_units.append(unit)

    def remove(self, unit:Unit):
        if unit in self.active_units:
            self.active_units.remove(unit)
            self.dead_units.append(unit)

    def print_allyUnits(self):
        console.print("[bold blue]아군 유닛 목록:")
        for u in self.ally_units:
            console.print(f" - [blue] [아군] {u.name}[/blue] (체력: {u.hp})")  

    def print_activeUnit(self):
        console.print("\n[bold yellow]현재 살아있는 유닛 목록:")
        for u in self.active_units:
            console.print(f" -[red] [적] {u.name}[/red] (체력: {u.hp})")

    def print_deadUnit(self):
        console.print("[bold gray]죽은 유닛 목록:")
        for u in self.dead_units:
            console.print(f" - {u.name}")

# 전역 유닛 매니저 인스턴스
unit_manager = UnitManager()

# =====================
#         유닛
# =====================

class Probe(Unit):
    def __init__(self):
        super().__init__('프로브', 50, 0, 1, 20, 20, 0, 'ground')

    def build(self, building:Building):
        console.print(f"[{self.name}]이(가) {building.name}을(를) 짓기 시작합니다.")
        with Progress(f"건설중...", BarColumn(), TaskProgressColumn(), SpinnerColumn(), TimeElapsedColumn()) as progress:
            task = progress.add_task(f"[cyan]{building.name} 건설 중...", total=building.build_time)
            while not progress.finished:
                time.sleep(0.1)
                progress.update(task, advance=0.1)
        console.print(f"[green]{building.name} 건설 완료!")
        return building

    def gather(self, resource):
        print(f'{self.name}이/가 {resource} 채집 중. . .')
        time.sleep(8)
        print(f'{resource} 채집 완료!')

# =====================
#       공격유닛
# =====================

class Zealot(AttackUnit):
    def __init__(self):
        super().__init__('질럿', 150, 0, 2, 40, 16, 40, 0, [0, 0], 10, [True, False], 0)

class Dragoon(AttackUnit):
    def __init__(self):
        super().__init__('드라군', 125, 25, 2, 100, 20, 40, 1, [0, 0], 15, [True, True], 0)

class HighTemplar(AttackUnit):
    def __init__(self):
        super().__init__('하이템플러', 50, 150, 2, 40, 0, 40, 0, [50, 150], 20, [False, False], 0)

    def psionic_storm(self, target:Unit):
        pass

class Archon(AttackUnit):
    pass

class DarkTemplar(AttackUnit):
    def __init__(self):
        super().__init__('다크템플러', 125, 100, 2, 80, 40, 40, 1, 20, [True, False], 0)

    def hide(self):
        pass

class DarkArchon(AttackUnit):
    def __init__(self):
        super().__init__('다크 아칸', 250, 200, 4, 25, 0, 200, 1, [50, 200], 30, [False, False], 0)
    
    def show_skill(self):
        console.print('마인드 컨트롤 - 마나 소모\n피드백 - 마나 소모')

    def mindcontrol(self, target):

        pass

    def peadback(self):
        pass

class Reaver(AttackUnit):
    def __init__(self):
        super().__init__('리버')

    def scarab(self):
        pass

# =====================
#         공 중
# =====================

class Scout(AttackUnit):
    def __init__(self):
        super().__init__('스카웃')

class Carrier(AttackUnit):
    def __init__(self):
        super().__init__()

class Corsair(AttackUnit):
    def __init__(self):
        super().__init__()

class Arbiter(AttackUnit):
    def __init__(self):
        super().__init__()


# =====================
#         건 물
# =====================

class Pylon(Building):
    def __init__(self):
        super().__init__('파일런', 100, 0, 10)

class GateWay(TrainingBuilding):
    def __init__(self):
        super().__init__('게이트 웨이', 150, 0, 20)

    def role(self):
        pass

class CyberneticsCore(ResearchBuilding):
    def __init__(self):
        super().__init__('사이버네틱스 코어', 200, 0, 20)

    def Dragoon_training(self):
        pass

    def fly_dmgUp(self):
        pass

    def fly_amrUp(self):
        pass

class forge(ResearchBuilding):
    def __init__(self):
        super().__init__('포지', 150, 0, 15)

    def ground_dmgUp(self):
        GDU1 = research('지상 공격력 증가 1', 100, 100, 60, False)
        GDU2 = research('지상 공격력 증가 2', 150, 150, 60, False)
        GDU3 = research('지상 공격력 증가 3', 200, 200, 60, False)

    def ground_armUp(self):
        pass

    def shieldUp(self):
        pass



# =================[ test ]====================

GDU1 = research('지상 공격력 증가 1', 100, 100, 60, False)
z = Zealot()
d = Dragoon()
h = HighTemplar()
g = GateWay()
f = forge()
# g.training(Zealot())
# g.training(DarkArchon())

f.research(GDU1)
unit_manager.allyRegister(z)
unit_manager.allyRegister(d)


unit_manager.register(z)
unit_manager.register(d)
unit_manager.register(h)
def game_time():
    while True:
        com = input('명령어 입력 (예: 공격 / 훈련)')
    pass

def attack_time():
    while True:
        command = input("명령어 입력 (예: 공격 / 목록 / 종료): ").strip()

        if command == '공격':
            unit_manager.print_allyUnits()
            ally = input('공격을 수행할 유닛 이름을 입력하세요: ')

            # 이름으로 유닛 찾기
            ally_name = None
            for unit in unit_manager.ally_units:
                if unit.name == ally:
                    ally_name = unit
                    break
            
            if ally_name:
                unit_manager.print_activeUnit()
                target = input('공격할 유닛 이름을 입력하세요: ')
                target_name = None
                for unit in unit_manager.active_units:
                    if unit.name == target:
                        target_name = unit
                        break

                if target_name:
                    ally_name.attack(target_name)
                else:
                    print(f"❌ {target} 유닛을 찾을 수 없습니다.")
            else:
                print(f"❌ {ally} 유닛을 찾을 수 없습니다.")
        
        elif command == '마법 공격':
            unit_manager.print_allyUnits()
            magically = input('마법 공격을 할 유닛 이름을 입력하세요: ')
            magically_name = None
            for u in unit_manager:
                if u.name == magically:
                    magically_name = u.name
                    break

            if magically_name:
                pass




        elif command == '목록':
            unit_manager.print_allyUnits()
            unit_manager.print_activeUnit()
            unit_manager.print_deadUnit()

        elif command == '종료':
            break

        else:
            print("⚠️ 잘못된 명령입니다. (공격 / 목록 / 종료 중 하나를 입력)")

attack_time()